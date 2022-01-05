#!/usr/bin/env bash



bgzip --version
if [ $? -ne 0 ]; then
  echo "htslib is required to manage variant files: installation instructions are at https://www.htslib.org/download/" 
  exit 1
fi

pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "make sure pip is installed" 
  exit 1
fi

# generate sample data
mkdir samples
cd samples
python ../generate_genomic.py
vcffiles=`ls *.vcf`
mkdir compressed
for f in $vcffiles
do
    bgzip -c $f > compressed/$f.gz
    tabix compressed/$f.gz
done

cd ..
docker cp samples/compressed candigv2_chord-metadata_1:/shared/
exit

# prep for ETL to katsu:
git clone https://github.com/CanDIG/medidata_mCode_ETL.git
cd medidata_mCode_ETL
git checkout daisieh/updates
pip install -r requirements.txt
cd ..

# prep data in mcode format:
python ../medidata_mCode_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2mcode/manifest.yml
docker cp Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json candigv2_chord-metadata_1:/shared/Synthetic_Clinical_Data_2_map_mcode.json

# ingest data into katsu
python katsu_ingest.py mohccn mcode-synthetic mcode-synthetic http://0.0.0.0:8008 /shared/Synthetic_Clinical_Data_2_map_mcode.json mcodepacket

# prep data in candigv1 format:
python ../medidata_mCode_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2candigv1/manifest.yml
docker cp Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json candigv2_chord-metadata_1:/shared/Synthetic_Clinical_Data_2_map_candigv1.json

# ingest data into candigv1

# load clinical data
docker exec candigv2_candig-server_1 ingest candig-example-data/registry.db 
mohccn /shared/Synthetic_Clinical_Data_2_map_candigv1.json

load reference data
docker exec candigv2_candig-server_1 wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
docker exec candigv2_candig-server_1 wget http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz.gzi
# docker exec candigv2_candig-server_1 gzip -d human_g1k_v37.fasta.gz
docker exec candigv2_candig-server_1 candig_repo add-referenceset candig-example-data/registry.db hs37d5.fa.gz \
    --description "NCBI37 assembly of the human genome" \
    --species '{"termId": "NCBI:9606", "term": "Homo sapiens"}' \
    --name hs37d5 \
    --sourceUri http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz

# load variant data
samples=`curl https://raw.githubusercontent.com/CanDIG/mohccn-data/main/Synthetic_Clinical%2BGenomic_data/ID_Matching_Table.csv`
first=0
Field_Separator=$IFS
IFS=$'\n\r'
for sample in $samples
do
    if [ $first -eq 0 ]; then
        first=1
    else
        val=`echo $sample | awk -F, '{print $3 " " $3 "_0 /shared/compressed/" $4 ".vcf.gz"}'`
        com="docker exec candigv2_candig-server_1 candig_repo add-variantset candig-example-data/registry.db mohccn $val -R hs37d5"
        echo $com
        eval $com
        # ingest data into htsget
        val=`echo $sample | awk -F, '{print "python htsget_ingest.py " $4 " /shared/compressed/ http://localhost:3333"}'`
        echo $val
        eval $val

    fi
done
IFS=Field_Separator

