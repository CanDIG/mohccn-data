#!/usr/bin/env bash

pip install -r requirements.txt

# generate sample data
mkdir samples
cd samples
python ../generate_genomic.py
cd ..

# ingest data into katsu
docker cp mCode_ingest_scripts.json candigv2_chord-metadata_1:/shared
python katsu_ingest.py mohccn mcode-synthetic --table mcode-synthetic --server_url http://0.0.0.0:8009 --data_file /shared/mCode_ingest_scripts.json --data_type mcodepacket
