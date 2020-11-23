#!/usr/bin/env python3

################################################
#
#   Script to filter only certain fields
#    from gnomAD datasource in vcf format
#
################################################

################################################
#   Libraries
################################################
import sys, argparse, os
import tabix

################################################
#   Functions
################################################
def parse_region(tb, region, fields_set, fo, c=0):
    ''' '''
    records = tb.querys(region)
    for record in records: #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
        c += 1
        sys.stderr.write('\r\t' + str(c))
        sys.stderr.flush()
        INFO_ = []
        INFO = record[7]
        # filtering INFO
        for field in INFO.split(';'):
            if field.split('=')[0] in fields_set:
                INFO_.append(field)
            #end if
        #end for
        record[7] = ';'.join(INFO_)
        fo.write('\t'.join(record) + '\n')
    #end for
    sys.stderr.write('\n')
#end def

def main(args):
    ''' '''
    # Variables
    chr = args['chr'] + ':'
    fields_set = set()

    # Buffers
    fo = open('trimmed_' + args['inputfile'].split('/')[-1].replace('.bgz', ''), 'w')
    tb = tabix.open(args['inputfile'])

    # Getting fields
    with open(args['fields']) as fi:
        for line in fi:
            fields_set.add(line.rstrip())
        #end for
    #end with

    # Reading chrom.sizes file
    with open(args['regionfile']) as fi:
        for line in fi:
            region = line.rstrip()
            if chr in region:
                sys.stderr.write(region + '\n')
                sys.stderr.flush()
                parse_region(tb, region, fields_set, fo)
            #end if
        #end for
    #end with

    fo.close()
#end def main

################################################
#   MAIN
################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-i', '--inputfile', help='input vcf file', required=True)
    parser.add_argument('-f', '--fields',  help='file with fields to save', required=True)
    parser.add_argument('-r', '--regionfile', help='regionfile', required=True)
    parser.add_argument('--chr', help='chromosome', required=True)

    args = vars(parser.parse_args())

    main(args)

#end if
