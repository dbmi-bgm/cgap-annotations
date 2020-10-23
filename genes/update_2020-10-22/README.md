### Files

#### gene_inserts_v0.4.6.json.gz:
original gene inserts file

#### gene_inserts_v0.4.6.updated.json.gz:
gene inserts file with updated `gene_summary` and `refseq_accession`

#### log_diff.txt:
log file with all changes for `gene_summary`

    CHANGE for <ENSGID>
        OLD: <summary | MISSING>
        NEW: <summary | DELETED>

#### log_id.txt:
log file with `ENSGID` not mapping to any `GeneID`

#### mapping.tsv:
mapping table between `GeneID`, `ENSGID`, `RSG`, `RNA_nucleotide_accession`.
`RSG` is a RefSeqGene accession (e.g. `NG_000000`).
`RNA_nucleotide_accession` is a RefSeq accession for RNA (e.g. `NM_000000`)

#### patch.tsv:
patch file for gene objects in the portal

    <ENSGID>    {'gene_summary': <summary>, 'refseq_accession': [<RSG | RNA_nucleotide_accession>, ...]}

`gene_summary: ''` means that a gene summary is missing and the key must be deleted.
`refseq_accession: []` means that there are no refseq accessions and the key must be deleted

#### summary.pickle:
pickle file storing summaries by RefSeq RNA accession or RefSeqGene accession

    {
      <RSG | RNA_nucleotide_accession>: <summary>,
      ...
    }
