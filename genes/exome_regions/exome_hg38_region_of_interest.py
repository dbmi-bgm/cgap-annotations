#!/usr/bin/env python3

import sys, csv

print('!!! The output of this file should be taken through a standard bedtools sort and bedtools merge before uploading to the portal as the exome bed region file !!!')
print('! Also note, this was designed to run on VEP v101 which does not contain chromosome names (e.g., 1 instead of chr1) !')

chrom = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','Y','X']

# input gft file
reader = csv.reader(open(sys.argv[1]), delimiter="\t")

# output file name
with open(sys.argv[2], 'w') as fout:
    for strLine in reader:
        #do not want header
        if "#!" not in strLine[0]:

            #only want main chromosomes
            if strLine[0] in chrom:

                #if the region is any exon (protein_coding, miRNA, processed transcript, etc.) write it out
                if strLine[2] == 'exon':
                        fout.write('chr' + strLine[0] + "\t" + str(int(strLine[3])-1)+ "\t" + str(strLine[4])+ "\n")

                #if the region is a UTR, write it out
                elif strLine[2] == 'three_prime_utr' or strLine[2] == 'five_prime_utr':
                    fout.write('chr' + strLine[0] + "\t" + str(int(strLine[3])-1) + "\t" + str(strLine[4]) + "\n")

    #also want to write the full mitochondrial genome
    fout.write('chrM' + "\t" + str(0) + "\t" + str(16569) + "\n")
