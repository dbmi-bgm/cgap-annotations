#!/usr/bin/env python3

################################################
#
#  Script specifically for reducing size of
#   dbSNP reference vcf files (no samples)
#   by making QUAL, FILTER, and INFO a "."
#
################################################

from granite.lib import vcf_parser
import sys

# $1 is input (vcf of vcf.gz), $2 is output (vcf)

in_vcf = vcf_parser.Vcf(sys.argv[1])

with open(sys.argv[2], 'w') as fo:
    in_vcf.write_header(fo)
    for vnt_obj in in_vcf.parse_variants():
        vnt_obj.QUAL = "."
        vnt_obj.FILTER = "."
        vnt_obj.INFO = "."
        in_vcf.write_variant(fo, vnt_obj)
