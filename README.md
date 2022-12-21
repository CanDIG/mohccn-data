# mohccn-data
Synthetic test data for MOHCCN

## NOTE: ingest scripts are now part of [candigv2-ingest](https://github.com/CanDIG/candigv2-ingest).

This repo contains test data and mappings for a couple of synthetic datasets. Mappings can be used with the [clinical_ETL tool](https://github.com/CanDIG/clinical_ETL_code) to create ingestable mcodepackets for Katsu.

The Makefile contains targets that demonstrate how to use this repo: `make split-subsets` uses the synthetic_clinical mapping on the sample data in the Synthetic_Clinical_Data_2 directory to create an ingestable file at Synthetic_Clinical_Data_2_map.json, then uses the split_subsets.py script to subdivide that file into three subsets, Synthetic_Clinical_Data_2_map_1.json, Synthetic_Clinical_Data_2_map_2.json, and Synthetic_Clinical_Data_2_map_3.json, with packets prefixed "SET#_" within.


## Setting a user to access this dataset:

Set user1 to have access to the mohccn dataset:

```bash
python opa_ingest.py --dataset mohccn --user user1@test.ca > access.json
docker cp access.json candigv2_opa_1:/app/permissions_engine/access.json
```


## Ingesting sample genomic files into a Docker setup

Make sure your env vars are set:

```bash
cd CanDIGv2
python settings.py
source env.sh
```

Then you should be able to run s3_ingest.py from candigv2-ingest:

```bash
python s3_ingest.py --samplefile ingest/files.txt --endpoint $MINIO_URL --bucket mohccndata --access $MINIO_ACCESS_KEY --secret $MINIO_SECRET_KEY
```

Now you should be able to ingest into htsget:

```bash
python htsget_s3_ingest.py --samplefile ingest/samples.txt --dataset mohccn --endpoint $MINIO_URL --bucket mohccndata --access $MINIO_ACCESS_KEY --secret $MINIO_SECRET_KEY --reference hg37 --indexing
```


## Ingesting clinical data into a Docker setup

Copy the data file to the katsu server, so that it is locally accessible:
```bash
docker cp ingest/Synthetic_Clinical_Data_2_map_2.json candigv2_chord-metadata_1:input.json
```

Then run the ingest tool:
```bash
python katsu_ingest.py --dataset mohccn --input /input.json
```

Repeat for a second dataset mohccn2:
```bash
docker cp ingest/Synthetic_Clinical_Data_2_map_3.json candigv2_chord-metadata_1:input.json
python katsu_ingest.py --dataset mohccn2 --input /input.json
```
