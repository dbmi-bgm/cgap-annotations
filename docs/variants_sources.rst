============
Data Sources
============

Software and data sources for variants annotation.

Vep
+++

*Current software version is 101.*

Annotation uses Vep software.

Source files for `Software`_ and `Plugins`_.

.. _Software: https://github.com/Ensembl/ensembl-vep/tree/release/101
.. _Plugins: https://github.com/Ensembl/VEP_plugins/tree/release/101

Annotation sources
------------------

Vep
^^^

This is the main annotation source for Vep.

Source file `v101`_ for homo_sapiens on GRCh38.

.. _v101: ftp://ftp.ensembl.org/pub/release-101/variation/vep/homo_sapiens_vep_101_GRCh38.tar.gz

MaxEnt
^^^^^^

*Current version v20040421.*

This is the data source used by ``MaxEntScan`` plugin.

Source file `fordownload`_.

.. _fordownload: http://hollywood.mit.edu/burgelab/maxent/download/fordownload.tar.gz

ClinVar
^^^^^^^

*Current version is v2020111. ClinVar is updated weekly.*

This is the data source for ClinVar to be used with ``--custom``.

.. code-block::

    # Compressed VCF file
    curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
    # Index file
    curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi

SpliceAI
^^^^^^^^

*Current version is v1.3.*

This is the data source used by ``SpliceAI`` plugin.

Download requires a log in on illumina platform and `BaseSpace sequence CLI`_.

.. _BaseSpace sequence CLI: https://developer.basespace.illumina.com/docs/content/documentation/cli/cli-overview

.. code-block::

    # Authenticate
    bs auth
    # Get id for dataset genome_scores
    bs list dataset
    # Download
    bs dataset download --id <datasetid> -o .

For annotation we are using the raw hg38 files and their index:

  - ``spliceai_scores.raw.snv.hg38.vcf.gz``
  - ``spliceai_scores.raw.indel.hg38.vcf.gz``

dbNSFP
^^^^^^

*Current version 4.1a.*

This is the data source used by ``dbNSFP`` plugin.

Source file `dbNSFP`_.

.. _dbNSFP: ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFP4.1a.zip

To create the data source:

.. code-block:: none

    > unzip dbNSFP4.1a.zip
    > zcat dbNSFP4.1a_variant.chr1.gz | head -n1 > h
    > zgrep -h -v ^#chr dbNSFP4.1a_variant.chr* | sort -T /path/to/tmp_folder -k1,1 -k2,2n - | cat h - | bgzip -c > dbNSFP4.1a.gz
    > tabix -s 1 -b 2 -e 2 dbNSFP4.1a.gz

gnomAD
^^^^^^

*Current version 3.1.*

File are available for download at https://gnomad.broadinstitute.org/downloads.

Files have been preprocessed to reduce the number of annotations.


Run Vep
-------

.. code-block:: none

    # base command
    vep \
    -i input.vcf \
    -o output.vep.vcf \
    --hgvs \
    --fasta <PATH/reference.fa> \
    --assembly GRCh38 \
    --use_given_ref \
    --offline \
    --cache_version 101 \
    --dir_cache . \
    --everything \
    --force_overwrite \
    --vcf \
    --dir_plugins <PATH/VEP_plugins>

    # additional plugins
    --plugin SpliceRegion,Extended
    --plugin MaxEntScan,<PATH/fordownload>
    --plugin TSSDistance
    --plugin dbNSFP,<PATH/dbNSFP.gz>,ALL
    --plugin SpliceAI,snv=<PATH/spliceai_scores.raw.snv.hg38.vcf.gz>,indel=<PATH/spliceai_scores.raw.indel.hg38.vcf.gz>

    # custom annotations
    --custom <PATH/clinvar.vcf.gz>,ClinVar,vcf,exact,0,ALLELEID,CLNSIG,CLNREVSTAT,CLNDN,CLNDISDB
    --custom <PATH/gnomAD.vcf.gz>,gnomADg,vcf,exact,0,AC,AC-XX,AC-XY,AC-afr,AC-ami,AC-amr,AC-asj,AC-eas,AC-fin,AC-mid,AC-nfe,AC-oth,AC-sas,AF,AF-XX,AF-XY,AF-afr,AF-ami,AF-amr,AF-asj,AF-eas,AF-fin,AF-mid,AF-nfe,AF-oth,AF-sas,AF_popmax,AN,AN-XX,AN-XY,AN-afr,AN-ami,AN-amr,AN-asj,AN-eas,AN-fin,AN-mid,AN-nfe,AN-oth,AN-sas,nhomalt,nhomalt-XX,nhomalt-XY,nhomalt-afr,nhomalt-ami,nhomalt-amr,nhomalt-asj,nhomalt-eas,nhomalt-fin,nhomalt-mid,nhomalt-nfe,nhomalt-oth,nhomalt-sas

Version
-------

*Current version accessed 2020-11-05.*

  - Vep: v101
  - MaxEnt: v20040421
  - ClinVar: v2020111
  - SpliceAI: v1.3
  - dbNSFP: v4.1a
  - gnomAD: v3.1
