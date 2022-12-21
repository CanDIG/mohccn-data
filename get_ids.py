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
    with requests.get("https://raw.githubusercontent.com/CanDIG/mohccn-data/main/Synthetic_Clinical_Data_2/ID_Matching_Table.csv") as r:
        for line in r.iter_lines(decode_unicode=True):
            print(line)
            if len(result.keys()) == 0:
                headers = line.split(",")
                for h in headers:
                    result[h] = []
            else:
                entries = line.split(",")
                for i in range(0,len(result.keys())):
                    result[list(result.keys())[i]].append(entries[i])
    if "str" in str(type(args)):
        return result[args]
    if "key" in args and args.key is not None:
        return result[args.key]
    return result

def main():
    parser = argparse.ArgumentParser(description="A script that gets ids from the ID matching table")
    parser.add_argument("key", help="column to get")
    args = parser.parse_args()
    return get_ids(args)

if __name__ == '__main__':
    print(json.dumps(get_ids(parse_args())))
