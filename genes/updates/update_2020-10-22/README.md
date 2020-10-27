### update
In v0.4.6 of genes annotations, there are errors with genes summaries that are missing or assigned to wrong genes.

v0.4.6 uses HGNC as the main source to retrieve refseq accessions associated with each gene.
However, HGNC still uses an older version of refseq and has inconsistencies with the current release, where obsolete accessions are updated or removed.
The data source is also partial being limited to only RefSeqGene.

This patch replaces HGNC and uses Ensembl identifiers to map each gene to the correct and up-to-date refseq accessions.
Gene summaries are associated with the correct genes and refseq accessions are updated fixing HGNC inconsistencies.
The patch also extends available annotations by including refseq for mRNA_prot on top of RefSeqGene.

### files in folder

#### gene_inserts_v0.4.6.json.gz
original gene inserts file

#### gene_inserts_v0.4.6.updated.json.gz
gene inserts file with updated `gene_summary` and `refseq_accession`

#### log_diff.txt
log file with all changes for `gene_summary`

    CHANGE for <ENSGID>
        OLD: <summary | MISSING>
        NEW: <summary | DELETED>

#### log_id.txt
log file with `ENSGID` not mapping to any `GeneID`

#### mapping.tsv
mapping table between `GeneID`, `ENSGID`, `RSG`, `RNA_nucleotide_accession`.
`RSG` is a RefSeqGene accession (e.g. `NG_000000`).
`RNA_nucleotide_accession` is a RefSeq accession for RNA (e.g. `NM_000000`)

#### patch.tsv
patch file for gene objects in the portal

    <ENSGID>    {'gene_summary': <summary>, 'refseq_accession': [<RSG | RNA_nucleotide_accession>, ...]}

`gene_summary: ''` means that a gene summary is missing and the key must be deleted.
`refseq_accession: []` means that there are no refseq accessions and the key must be deleted

#### summary.pickle
pickle file storing summaries by RefSeq RNA accession or RefSeqGene accession

    {
      <RSG | RNA_nucleotide_accession>: <summary>,
      ...
    }

### command
files have been generate using patching_refseq.py (in scripts)

    ./patching_refseq.py \
        --gene_inserts gene_inserts_v0.4.6.json \
        --LRG_RefSeqGene LRG_RefSeqGene \
        --gene2ensembl gene2ensembl \
        --gene2refseq gene2refseq \
        --sourcefile refseqgene.1.genomic.gbff refseqgene.2.genomic.gbff refseqgene.3.genomic.gbff refseqgene.4.genomic.gbff refseqgene.5.genomic.gbff \
                     human.1.rna.gbff human.2.rna.gbff human.3.rna.gbff human.4.rna.gbff human.5.rna.gbff human.6.rna.gbff human.7.rna.gbff human.8.rna.gbff

source files are available in `s3://cgap-annotations/RefSeq/RefSeq_2020-10-22`
