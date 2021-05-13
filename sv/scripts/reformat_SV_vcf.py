#!/usr/bin/env python3

################################################
#
#    Script to add FORMAT and contig fields to
#    the header of VCF files from Parliament2
#
################################################

################################################
#   Libraries
################################################

from granite.lib import vcf_parser
import sys, argparse, subprocess

################################################
#   Functions
################################################

def main(args):
    # open input VCF for parsing
    vcf = vcf_parser.Vcf(args['inputVCF'])

    # pull contig fields from reference file and add them to VCF header
    with open(args['inputContig'],'r') as contigs:
        for contig_line in contigs:
            vcf.header.add_tag_definition(contig_line.strip('\n'))

    # add FORMAT field for SP to VCF header
    SP = '##FORMAT=<ID=SP,Number=.,Type=String,Description="Names of SV callers that identified this variant">'
    vcf.header.add_tag_definition(SP)

    # write reformatted header and all variants
    with open(args['outputfile'], 'w') as fo:
        vcf.write_header(fo)
        for vnt_obj in vcf.parse_variants():
            vcf.write_variant(fo, vnt_obj)

    subprocess.run(["bgzip", args['outputfile']])

################################################
#   Main
################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Reformat SV VCF file following Parliament2 and Survivor')

    parser.add_argument('-i','--inputVCF', help='input VCF file', required=True)
    parser.add_argument('-c','--inputContig', help='input reference file with contigs', required=True)
    parser.add_argument('-o','--outputfile', help='output VCF file', required=True)

    args = vars(parser.parse_args())

    main(args)
