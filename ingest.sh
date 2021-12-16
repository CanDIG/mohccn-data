#!/usr/bin/env bash

pip install -r requirements.txt

# generate sample data
mkdir samples
cd samples
python ../generate_genomic.py
cd ..

# prep for ETL to katsu:
git clone https://github.com/CanDIG/medidata_mCode_ETL.git
cd medidata_mCode_ETL
git checkout daisieh/updates
pip install -r requirements.txt
cd ..

# prep data in candigv1 format:
python ../medidata_mCode_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2candigv1/manifest.yml
mv Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json /shared/Synthetic_Clinical_Data_2_map_v1.json

# prep data in mcode format:
python ../medidata_mCode_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2mcode/manifest.yml
mv Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json /shared/Synthetic_Clinical_Data_2_map_mcode.json

# ingest data into candigv1


# ingest data into katsu
python katsu_ingest.py mohccn mcode-synthetic mcode-synthetic http://0.0.0.0:8009 /shared/Synthetic_Clinical_Data_2_map_mcode.json mcodepacket
