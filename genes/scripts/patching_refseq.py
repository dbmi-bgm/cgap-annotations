#!/usr/bin/env python3

################################################
#
#   Script to patch gene inserts json file
#
################################################

################################################
#   Libraries
################################################
import sys, argparse, os
import json
import re
import pickle
from Bio import SeqIO

################################################
#   Functions
################################################
def parse_sourcefile(filename, summary, c=0):
    ''' '''
    records = SeqIO.parse(filename, "genbank")
    sys.stderr.write('\t' + filename + '\n')
    for record in records:
        c += 1
        sys.stderr.write('\r\t\tn. ' + str(c))
        sys.stderr.flush()
        comment = record.annotations['comment'].replace('\n', ' ')
        if 'Summary:' in comment:
            gene_summary = re.search('Summary:(.+?\]\.)', comment)
            # contains also 'Summary:', the description only is in group(1)
            summary.setdefault(record.name, gene_summary.group(1).strip())
        #end if
    #end for
    sys.stderr.write('\n')
    sys.stderr.flush()
# end def

def main(args):

    #note: the nucleotide_accession from HGNC that are not mapping are either been removed
    #      or replaced in RefSeq. It is possible to rescue most of them using ENSG instead
    #      to map to the GeneID. However this may lead to results that are not consistent
    #      with how the gene is defined in HGNC.

    # data structures
    ENSG_map = {} # {ENSG: GeneID, ...}
    GeneID_map = {} # {GeneID: {ENSG: ENSG,
                    #        rsg: genomic_nucleotide_accession, <from RefSeqGene>
                    #        rna: set(RNA_nucleotide_accession, ...)}, ...}
    summary = {} # {genomic_nucleotide_accession: Summary} <from RefSeqGene>

    # loading gene inserts
    with open(args['gene_inserts']) as fi:
        gene_inserts = json.load(fi)
    #end with
    sys.stderr.write('loaded gene_inserts...\n')
    sys.stderr.flush()

    # gene2refseq
    # initialize GeneID_map
    # header:
        #tax_id [9606]
        #GeneID [163081]
        #status [VALIDATED]
        #RNA_nucleotide_accession.version [NM_152603.5]
        #RNA_nucleotide_gi [1677498178]
        #protein_accession.version [NP_689816.2]
        #protein_gi [34303941]
        #genomic_nucleotide_accession.version [NC_000019.10]
        #genomic_nucleotide_gi [568815579]
        #start_position_on_the_genomic_accession [36666960]
        #end_position_on_the_genomic_accession [36723547]
        #orientation [-]
        #assembly [-]
        #mature_peptide_accession.version [-]
        #mature_peptide_gi [-]
        #Symbol [ZNF567]
    with open(args['gene2refseq']) as fi:
        for line in fi:
            if not line.startswith('#'):
                line_split = line.rstrip().split('\t')
                if line_split[0] == '9606': #check tax_id
                    GeneID, status, RNA_na = line_split[1], line_split[2], line_split[3]
                    GeneID_map.setdefault(GeneID, {'ENSG': '-',
                                                   'rsg': '-',
                                                   'rna': set()})
                    if RNA_na and RNA_na not in ['.', '-'] and status != 'SUPPRESSED':
                        GeneID_map[GeneID]['rna'].add(RNA_na.split('.')[0])
                    #end if
                #end if
            #end if
        #end for
    #end with
    sys.stderr.write('loaded gene2refseq...\n')
    sys.stderr.flush()

    # gene2ensembl
    # map Ensembl_gene_identifier to GeneID in ENSG_map
    # map GeneID to Ensembl_gene_identifier in GeneID_map
    # header:
        #tax_id [9606]
        #GeneID [29974]
        #Ensembl_gene_identifier [ENSG00000148584]
        #RNA_nucleotide_accession.version [NM_001198819.2]
        #Ensembl_rna_identifier [ENST00000395489.6]
        #protein_accession.version [NP_001185748.1]
        #Ensembl_protein_identifier [ENSP00000378868.3]
    with open(args['gene2ensembl']) as fi:
        for line in fi:
            if not line.startswith('#'):
                tax_id, GeneID, ENSG, RNA_na, _, _, _ = line.rstrip().split('\t')
                if tax_id == '9606':
                    ENSG_map.setdefault(ENSG, GeneID)
                    GeneID_map[GeneID]['ENSG'] = ENSG
                    if RNA_na and RNA_na not in ['.', '-']:
                        GeneID_map[GeneID]['rna'].add(RNA_na.split('.')[0])
                    #end if
                #end if
            #end if
        #end for
    #end with
    sys.stderr.write('loaded gene2ensembl...\n')
    sys.stderr.flush()

    # LRG_RefSeqGene
    # map GeneID to genomic_nucleotide_accession in GeneID_map
    # header:
        #tax_id [9606]
        #GeneID [16]
        #Symbol [AARS1]
        #RSG [NG_023191.1]
        #LRG [LRG_359]
        #RNA [NM_001605.2]
        #t [t1]
        #Protein [NP_001596.2]
        #p [p1]
        #Category [reference standard]
    with open(args['LRG_RefSeqGene']) as fi:
        for line in fi:
            if not line.startswith('#'):
                _, GeneID, _, genomic_na, _, RNA_na, _, _, _, _ = line.rstrip().split('\t')
                GeneID_map[GeneID]['rsg'] = genomic_na.split('.')[0]
                if RNA_na and RNA_na not in ['.', '-']:
                    GeneID_map[GeneID]['rna'].add(RNA_na.split('.')[0])
                #end if
            #end if
        #end for
    #end with
    sys.stderr.write('loaded LRG_RefSeqGene...\n')
    sys.stderr.flush()

    # getting summaries from sourcefile
    if args['sourcefile']:
        for filename in args['sourcefile']:
            parse_sourcefile(filename, summary)
        #end for
        # save summary as pickle file
        with open("summary.pickle", "wb") as fo:
            pickle.dump(summary, fo)
        #end with
    # getting saved summary as pickle file
    elif args['summarydict']:
        with open(args['summarydict'], 'rb') as fi:
            summary = pickle.load(fi)
        #end with
    else:
        sys.exit('specify either --sourcefile or --summarydict argument\n')
    #end if
    sys.stderr.write('loaded sourcefile...\n')
    sys.stderr.flush()

    # write mappig table
    with open('mapping.tsv', 'w') as fo:
        fo.write('#GeneID\tEnsembl_gene_identifier\tRefSeqGene\tRNA_nucleotide_accessions\n')
        for GeneID, value in sorted(GeneID_map.items(), key=lambda x: int(x[0])):
            if value['ENSG'] != '-':
                value_rna = '-'
                if value['rna']: value_rna = ','.join(sorted(value['rna']))
                #end if
                fo.write('{0}\t{1}\t{2}\t{3}\n'.format(
                                                    GeneID,
                                                    value['ENSG'],
                                                    value['rsg'],
                                                    value_rna
                                                ))
            #end if
        #end for
    #end with

    # buffers out
    fl = open('log_id.txt', 'w')
    fc = open('log_diff.txt', 'w')

    # update genes from gene_inserts
    patch_json = {}
    for gene in gene_inserts:
        ensgid = gene['ensgid']
        gene_summary = set()
        rs_accession = set()
        patch_dict = {}
        if ensgid in ENSG_map:
            GeneID = ENSG_map[ensgid]
            if GeneID in GeneID_map:
                rsg = GeneID_map[GeneID]['rsg']
                if rsg in summary:
                    gene_summary.add(summary[rsg])
                    rs_accession.add(rsg)
                #end if
                if 'refseq_accession' in gene:
                    for rna in gene['refseq_accession']:
                        rna_ = rna.split('.')[0]
                        if rna_ in GeneID_map[GeneID]['rna']:
                            rs_accession.add(rna_)
                            if rna_ in summary:
                                gene_summary.add(summary[rna_])
                            #end if
                        #end if
                    #end for
                #end if
                if gene_summary:
                    gene_summary_join = '\n'.join(sorted(gene_summary))
                    if 'gene_summary' in gene:
                        if gene['gene_summary'] != gene_summary_join:
                            fc.write('CHANGE for ' + ensgid + '\n\t')
                            fc.write('OLD: ' + gene['gene_summary'] + '\n\t')
                            fc.write('NEW: ' + gene_summary_join.replace('\n', ' | ') + '\n')
                        #end if
                    else:
                        fc.write('CHANGE for ' + ensgid + '\n\t')
                        fc.write('OLD: MISSING\n\t')
                        fc.write('NEW: ' + gene_summary_join.replace('\n', ' | ') + '\n')
                    #end if
                    gene['gene_summary'] = gene_summary_join
                    patch_dict['gene_summary'] = gene_summary_join
                else:
                    if 'gene_summary' in gene:
                        patch_dict['gene_summary'] = ''
                        fc.write('CHANGE for ' + ensgid + '\n\t')
                        fc.write('OLD: ' + gene['gene_summary'] + '\n\t')
                        fc.write('NEW: DELETED\n')
                        del gene['gene_summary']
                    #end if
                #end if
                if rs_accession:
                    rs_accession_list = list(sorted(rs_accession))
                    gene['refseq_accession'] = rs_accession_list
                    patch_dict['refseq_accession'] = rs_accession_list
                else:
                    if 'refseq_accession' in gene:
                        patch_dict['refseq_accession'] = []
                        del gene['refseq_accession']
                    #end if
                #end if
                if patch_dict:
                    patch_json.setdefault(ensgid, patch_dict)
                #end if
            else:
                fl.write('MISSING RefSeq for ' + ensgid + '\n')
                continue
            #end if
        else: # these are obsolete
            if 'refseq_accession' in gene:
                fl.write('MISSING GeneID for ' + ensgid + ', has refseq_accession\n')
                patch_dict['refseq_accession'] = []
                del gene['refseq_accession']
            else:
                fl.write('MISSING GeneID for ' + ensgid + '\n')
            #end if
            if 'gene_summary' in gene:
                patch_dict['gene_summary'] = ''
                del gene['gene_summary']
            #end if
            if patch_dict:
                patch_json.setdefault(ensgid, patch_dict)
            #end if
            continue
        #end if
    #end for

    # saving updated json
    outname = args['gene_inserts'].split('/')[-1].split('.json')[0] + '.updated.json'
    with open(outname, 'w') as fo:
        json.dump(gene_inserts, fo, indent=1)
    #end with

    with open('patch.json', 'w') as fo:
        json.dump(patch_json, fo, indent=1)
    #end with

    # closing buffers out
    fl.close()
    fc.close()
#end def main

################################################
#   MAIN
################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--gene_inserts', help='gene inserts file in json format', required=True)
    parser.add_argument('--LRG_RefSeqGene', help='LRG_RefSeqGene mapping file', required=True)
    parser.add_argument('--gene2ensembl', help='gene2ensembl mapping file', required=True)
    parser.add_argument('--gene2refseq', help='gene2refseq mapping file', required=True)
    parser.add_argument('--sourcefile', help='gbff file to use as source, it is possible to list multiple files', nargs='+', required=False)
    parser.add_argument('--summarydict', help='dict of gene_summary in pickle format', required=False)

    args = vars(parser.parse_args())

    main(args)

#end if
