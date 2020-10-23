
##### gene_inserts_v0.4.6.json.gz
original gene inserts file

##### gene_inserts_v0.4.6.updated.json.gz
gene inserts file with updated `gene_summary` and `refseq_accession`

##### log_diff.txt
log file with all changes for `gene_summary`

    CHANGE for <ENSGID>
        OLD: <old gene_summary | MISSING>
        NEW: <new gene_summary | DELETED>

##### log_id.txt
log file with `ENSGID` not mapping to any `GeneID`

##### mapping.tsv
mapping table between `GeneID`, `ENSGID`, `RSG` (RefSeqGene), `RNA_nucleotide_accession` (mRNA_Prot)

##### patch.tsv
patch file for gene objects in the portal

    <ENSGID>    {'gene_summary': <gene_summary | ''>, 'refseq_accession': <[NG_, NM_, ...] | []>}

`gene_summary: ''` means that a gene summary is missing and the key must be deleted

`refseq_accession: []` means that there are no refseq accessions and the key must be deleted

##### summary.pickle
pickle file storing gene summaries by

    {
      <RSG | RNA_nucleotide_accession>: <gene_summary>,
      ...
    }
