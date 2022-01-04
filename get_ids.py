import re
import requests
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, help="Specific key to return")
    args = parser.parse_args()
    return args


def get_ids(args):
    thou_gen_ids = []
    result = {}
    with requests.get("https://raw.githubusercontent.com/CanDIG/mohccn-data/main/Synthetic_Clinical%2BGenomic_data/ID_Matching_Table.csv") as r:
        for line in r.iter_lines(decode_unicode=True):
            if len(result.keys()) == 0:
                headers = line.split(",")
                for h in headers:
                    result[h] = []
            else:
                entries = line.split(",")
                for i in range(0,len(result.keys())):
                    result[list(result.keys())[i]].append(entries[i])
    if args.key is not None:
        return result[args.key]
    return result


if __name__ == '__main__':
    print(json.dumps(get_ids(parse_args())))
