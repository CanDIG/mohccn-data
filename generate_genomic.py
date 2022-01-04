import re
import requests
import get_ids


## Generate single-sample VCF files for the samples listed in https://github.com/CanDIG/mohccn-data/blob/main/Synthetic_Clinical%2BGenomic_data/ID_Matching_Table.csv.
## We're using a small segment of chr21 (9000000-10000000) as the test region.



def get_variant_obj(chrom, start, end, ids):
    result = None
    urls = []
    file_url_objs = []
    header = ""
    samples = []
    with requests.get(f"https://htsget.ga4gh.org/variants/1000genomes.phase1.chr{chrom}?format=VCF&referenceName={chrom}&start={start}&end={end}") as r:
        print(r.json())
        urls = r.json()["htsget"]["urls"]
    for url_obj in urls:
        if "class" in url_obj and url_obj["class"] == "header":
            with requests.get(url_obj["url"], headers=url_obj["headers"], stream=True) as r:
                for line in r.iter_lines(decode_unicode=True):
                    sample_match = re.match("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t(.+)", line)
                    if sample_match is not None:
                        samples = sample_match.group(1).split("\t")
                    else:
                        header += line + "\n"
        if "class" in url_obj and url_obj["class"] == "body":
            file_url_objs.append(url_obj)
        
        for sample_id in ids:
            id_index = samples.index(sample_id)
            with open(f"{sample_id}.vcf", mode="w") as f:
                f.write(header)
                f.write('##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position">')
                f.write(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{sample_id}\n")
        for url_obj in file_url_objs:
            with requests.get(url_obj["url"], stream=True, headers=url_obj["headers"]) as r:
                for line in r.iter_lines(decode_unicode=True):
                    #test_match = re.match("(.+?)\t(.+?)\t.+?\t.+?\t(.+?)\t.+?\t.+?\t.+?\t.+?\t(.+)", line)
                    #annotation = get_annotation(test_match.group(1), test_match.group(2), test_match.group(3))
                    for sample_id in ids:
                        id_index = samples.index(sample_id)
                        with open(f"{sample_id}.vcf", mode="a") as f:
                            sample_match = re.match("(.+?\t.+?\t.+?\t.+?\t.+?\t.+?\t.+?\t.+?\t.+?)\t(.+)", line)
                            if sample_match is not None:
                                sample = sample_match.group(2).split("\t")[id_index]
                                f.write(f"{sample_match.group(1)}\t{sample}\n")


# def get_annotation(chrom, loc, allele):
#     headers = {"Content-Type": "application/json"}
#     url = f"https://rest.ensembl.org/vep/human/region/{chrom}:{loc}/{allele}"
#     with requests.get(url, headers=headers) as r:
#         ##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position">
#         anno = r.json()
#         result = anno['intergenic_consequences'][0]['variant_allele'] + "|"
#         result += anno['intergenic_consequences'][0]['consequence_terms'].split(",")


if __name__ == '__main__':
    thou_gen_ids = get_ids.get_ids()["1000 Genomes_ID"]
    get_variant_obj(21, 9000000, 9500000, thou_gen_ids)

