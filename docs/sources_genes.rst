=====
Genes
=====

Data sources available for genes.

RefSeq
++++++

*Current version accessed 22-10-2020.*

Files
-----

ncbi refseq `RefSeqGene`_:

.. _RefSeqGene: https://ftp.ncbi.nih.gov/refseq/H_sapiens/RefSeqGene/

  - LRG_RefSeqGene
  - refseqgene.<n>.genomic.gbff.gz

ncbi refseq `mRNA_Prot`_:

.. _mRNA_Prot: https://ftp.ncbi.nih.gov/refseq/H_sapiens/mRNA_Prot/

  - human.<n>.rna.gbff.gz

ncbi `gene`_:

.. _gene: https://ftp.ncbi.nih.gov/gene/DATA/

  - gene2ensembl.gz
  - gene2refseq.gz

Description
-----------

`LRG_RefSeqGene` is a tab-delimited file reporting, for each gene, the *accession.version* of the genomic RefSeq (RSG) that is the standard reference.
Additionally reports the *accession.version* of the associated RNA and protein RefSeqs.

::

    #tax_id   GeneID   Symbol   RSG    LRG   RNA    t   Protein   p   Category

`refseqgene.<n>.genomic.gbff` report annotations for each RSG in GenBank format.

`human.<n>.rna.gbff` report annotations for each RNA and protein RefSeq in GenBank format.

`gene2ensembl` is a tab-delimited file matching NCBI to Ensembl annotations.

::

    #tax_id   GeneID   Ensembl_gene_identifier   RNA_nucleotide_accession.version   Ensembl_rna_identifier   protein_accession.version   Ensembl_protein_identifier

`gene2refseq` is a tab-delimited file reporting genomic/RNA/protein sets of matching RefSeqs.

::

    #tax_id   GeneID   status   RNA_nucleotide_accession.version   RNA_nucleotide_gi   protein_accession.version   protein_gi   genomic_nucleotide_accession.version   genomic_nucleotide_gi   start_position_on_the_genomic_accession   end_position_on_the_genomic_accession   orientation   assembly   mature_peptide_accession.version   mature_peptide_gi   Symbol
