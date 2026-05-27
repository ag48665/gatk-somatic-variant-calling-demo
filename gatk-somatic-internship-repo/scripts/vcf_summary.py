#!/usr/bin/env python3
import argparse
import gzip
from collections import Counter


def open_text(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "r", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Summarize PASS and filtered variants in a VCF.")
    parser.add_argument("vcf")
    args = parser.parse_args()
    counts = Counter()
    with open_text(args.vcf) as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            counts[line.rstrip().split("\t")[6]] += 1
    print("filter\tcount")
    for key, value in sorted(counts.items()):
        print(f"{key}\t{value}")


if __name__ == "__main__":
    main()
