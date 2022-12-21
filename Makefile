#!make

samples/*.vcf: | /samples
	@echo "generating..."
	$(shell cd samples; python ../generate_genomic.py)

/samples:
	@mkdir -p $(PWD)/samples

Synthetic_Clinical_Data_2_map.json:
	python clinical_ETL_code/CSVConvert.py --manifest mappings/synthetic_clinical/manifest.yml --input Synthetic_Clinical_Data_2

.PHONY: split-subsets
split-subsets: Synthetic_Clinical_Data_2_map.json
	python split_subsets.py Synthetic_Clinical_Data_2_map.json -n 3
