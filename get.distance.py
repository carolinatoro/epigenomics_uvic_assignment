#!/usr/bin/env python3

import sys
from optparse import OptionParser

#************
# OPTION PARSING *
#************
parser = OptionParser()
parser.add_option("-i", "--input", dest="input", help="File with gene start coordinates")
parser.add_option("-s", "--start", dest="start", help="Start coordinate of a single regulatory element")
parser.add_option("-b", "--batch", dest="batch", help="Optional file with multiple regulatory elements (tab-separated: name and start coordinate)")

options, args = parser.parse_args()

# Load gene start positions into memory
gene_positions = []
with open(options.input) as f:
    for line in f:
        gene, pos = line.strip().split('\t')
        gene_positions.append((gene, int(pos)))

# Function to find closest gene
def find_closest_gene(enhancer_start):
    min_distance = 1000000  # 1Mb max distance
    selected_gene = ""
    selected_gene_start = 0

    for gene, pos in gene_positions:
        distance = abs(pos - enhancer_start)
        if distance < min_distance:
            min_distance = distance
            selected_gene = gene
            selected_gene_start = pos

    return selected_gene, selected_gene_start, min_distance

#********
# BATCH MODE
#********
if options.batch:
    with open(options.batch) as f:
        for line in f:
            region, start = line.strip().split('\t')
            start = int(start)
            gene, gene_start, distance = find_closest_gene(start)
            print(f"{region}\t{gene}\t{gene_start}\t{distance}")
    sys.exit(0)

#********
# SINGLE MODE (Default)
#********
if options.start is None:
    print("Error: Please provide either --start for single mode or --batch for batch mode.", file=sys.stderr)
    sys.exit(1)

enhancer_start = int(options.start)
gene, gene_start, distance = find_closest_gene(enhancer_start)
print(f"{gene}\t{gene_start}\t{distance}")
