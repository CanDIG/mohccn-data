#!make

samples/*.vcf: | /samples
	@echo "generating..."
	$(shell cd samples; python ../generate_genomic.py)

samples/*.gz.tbi: | /samples
ifeq (, $(shell which bgzip))
$(error "bgzip is part of htslib; htslib is required to manage variant files: installation instructions are at https://www.htslib.org/download/")
endif
$(foreach F, $(wildcard samples/*.vcf), $(shell bgzip $(F); tabix $(F).gz))

/samples:
	@mkdir -p $(PWD)/samples

hs37d5.fa.gz: 
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz --output hs37d5.fa.gz

hs37d5.fa.gz.gzi:
	curl http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz.gzi --output hs37d5.fa.gz.gzi