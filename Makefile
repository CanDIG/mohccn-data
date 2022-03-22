#!make

# import global variables
CANDIG_HOME ?= ../CanDIGv2
env ?= $(CANDIG_HOME)/.env

include $(env)
export $(shell sed 's/=.*//' $(env))

SHELL = bash
DIR = $(PWD)
KATSU = $(shell docker ps --format "{{.Names}}" | grep "chord-metadata")
HTSGET=$(shell docker ps --format "{{.Names}}" | grep "htsget")
CANDIG_SERVER=$(shell docker ps --format "{{.Names}}" | grep "candig-server")

.PHONY: all
all: copy-samples katsu_ready candig_server_ready
	@./ingest.sh
	
.PHONY: copy-samples
copy-samples: samples/*.gz.tbi
	docker cp samples $(KATSU):samples
	docker cp samples $(HTSGET):samples
	docker cp samples $(CANDIG_SERVER):samples

samples/*.vcf: | /samples
	@echo "generating..."
	$(shell cd samples; python ../generate_genomic.py)

samples/*.gz.tbi: | samples/*.vcf 
ifeq (, $(shell which bgzip))
$(error "bgzip is part of htslib; htslib is required to manage variant files: installation instructions are at https://www.htslib.org/download/")
endif
	@echo "compressing... $(wildcard samples/*.vcf)"
$(foreach F, $(wildcard samples/*.vcf), $(shell bgzip -i $(F)))

/samples:
	@mkdir -p $(DIR)/samples

clinical_ETL_ready:
	git clone https://github.com/CanDIG/clinical_ETL.git
	@pip install -r clinical_ETL/requirements.txt
	@pip install -r requirements.txt
	@touch clinical_ETL_ready

reference_loaded: hs37d5.fa.gz hs37d5.fa.gz.gzi
	@echo "loading reference data"
	docker cp hs37d5.fa.gz $(CANDIG_SERVER):/app/candig-server
	docker cp hs37d5.fa.gz.gzi $(CANDIG_SERVER):/app/candig-server
	docker exec $(CANDIG_SERVER) candig_repo add-referenceset candig-example-data/registry.db hs37d5.fa.gz \
		--description "NCBI37 assembly of the human genome" \
		--species '{"termId": "NCBI:9606", "term": "Homo sapiens"}' \
		--name hs37d5 \
		--sourceUri http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz
	@touch reference_loaded

hs37d5.fa.gz: 
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz --output hs37d5.fa.gz

hs37d5.fa.gz.gzi:
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz.gzi --output hs37d5.fa.gz.gzi

katsu_ready: | clinical_ETL_ready
	python clinical_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2mcode/manifest.yml
	docker cp Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json $(KATSU):Synthetic_Clinical_Data_2_map_mcode.json
	python katsu_ingest.py mohccn mcode-synthetic mcode-synthetic $(CHORD_METADATA_PUBLIC_URL) /Synthetic_Clinical_Data_2_map_mcode.json mcodepacket
	@touch katsu_ready

candig_server_ready: | clinical_ETL_ready reference_loaded
	python clinical_ETL/CSVConvert.py --input Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2.xlsx --mapping mappings/synthetic2candigv1/manifest.yml
	docker cp Synthetic_Clinical+Genomic_data/Synthetic_Clinical_Data_2_map.json $(CANDIG_SERVER):Synthetic_Clinical_Data_2_map_candigv1.json
	docker exec $(CANDIG_SERVER) ingest candig-example-data/registry.db mohccn /Synthetic_Clinical_Data_2_map_candigv1.json
	@touch candig_server_ready

.PHONY: clean
clean:
	rm -f candig_server_ready
	rm -f katsu_ready
	rm -f hs37d5.fa.gz*
	rm -f reference_loaded
	rm -Rf samples
	rm -Rf clinical_ETL*
