#!/usr/bin/env python

################################################
#
#   Script to filter only certain fields
#    from gnomAD v2.1 exome in vcf format
#
################################################

# This script is much simpler than filter_gnomAD.py since that parsed v3.1 genomic data where many chromsomes were larger than the entire exome vcf for v2.1
# The exome data for v2.1 was filtered on a single CPU within a few hours

from granite.lib import vcf_parser
import sys

input = sys.argv[1] # gnomad.exomes.r2.1.1.sites.liftover_grch38.vcf.bgz
fields_file = sys.argv[2] #gnomAD_2.1_fields.tsv

vcf = vcf_parser.Vcf(input)

fields_set = set()
with open(fields_file) as fi:
    for line in fi:
        fields_set.add(line.rstrip())

with open('trimmed_' + input.split('/')[-1].replace('.bgz', '').replace('.gz', ''), 'w') as fo:
    vcf.write_header(fo)
    c = 0
    for vnt_obj in vcf.parse_variants():
        c += 1
        sys.stderr.write('\r\t' + str(c))
        sys.stderr.flush()
        INFO = vnt_obj.INFO
        INFO_ = []
        for field in INFO.split(';'):
            if field.split('=')[0] in fields_set:
                INFO_.append(field)
        vnt_obj.INFO = ';'.join(INFO_)
        vcf.write_variant(fo, vnt_obj)
