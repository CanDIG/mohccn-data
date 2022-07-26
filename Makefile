#!make

samples/*.vcf: | /samples
	@echo "generating..."
	$(shell cd samples; python ../generate_genomic.py)

/samples:
	@mkdir -p $(PWD)/samples

hs37d5.fa.gz: 
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz --output hs37d5.fa.gz

hs37d5.fa.gz.gzi:
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz.gzi --output hs37d5.fa.gz.gzi

Synthetic_Clinical_Data_2_map.json:
	python clinical_ETL_code/CSVConvert.py --manifest mappings/synthetic_clinical/manifest.yml --input Synthetic_Clinical_Data_2

.PHONY: split-subsets
split-subsets: Synthetic_Clinical_Data_2_map.json
	python split_subsets.py Synthetic_Clinical_Data_2_map.json -n 3
