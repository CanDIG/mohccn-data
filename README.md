# mohccn-data
Synthetic test data for MOHCCN

## NOTE: ingest scripts are now part of [candigv2-ingest](https://github.com/CanDIG/candigv2-ingest).

This repo contains test data and mappings for a couple of synthetic datasets. Mappings can be used with the [clinical_ETL tool](https://github.com/CanDIG/clinical_ETL_code) to create ingestable mcodepackets for Katsu.

The Makefile contains targets that demonstrate how to use this repo: `make split-subsets` uses the synthetic_clinical mapping on the sample data in the Synthetic_Clinical_Data_2 directory to create an ingestable file at Synthetic_Clinical_Data_2_map.json, then uses the split_subsets.py script to subdivide that file into three subsets, Synthetic_Clinical_Data_2_map_1.json, Synthetic_Clinical_Data_2_map_2.json, and Synthetic_Clinical_Data_2_map_3.json, with packets prefixed "SET#_" within.