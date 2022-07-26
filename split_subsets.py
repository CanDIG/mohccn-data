import re
import requests
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Split a mcodepacket file into subsets")
    parser.add_argument("input", help="file to split")
    parser.add_argument("-n", help="how many subsets to create")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    num = int(args.n)

    subsets = []
    with open(args.input) as f:
        packets = json.load(f)
        if len(packets)/num < 1:
            print("The input file has fewer mcodepackets than requested subsets.")
            return
        # set up
        for i in range(0,num):
            subsets.append([])
        for i in range(0, len(packets)):
            subset = i%num
            packet = packets[i]
            id = packet["id"]
            packet_str = json.dumps(packet)
            subsets[subset].append(json.loads(packet_str.replace(id, f"SET{subset+1}_{id}")))

    if len(subsets) == 0:
        print(f"No subsets were created: check format of input file {args.input}")
        return
        
    for i in range(0, len(subsets)):
        with open(f"{args.input.replace('.json','')}_{i+1}.json", 'w') as f:
            json.dump(subsets[i], f, indent=4)


if __name__ == '__main__':
    main()
