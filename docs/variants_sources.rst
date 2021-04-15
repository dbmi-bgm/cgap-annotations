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

.. code-block:: bash

    $ wget ftp://ftp.ensembl.org/pub/release-101/variation/vep/homo_sapiens_vep_101_GRCh38.tar.gz

MaxEnt
^^^^^^

*Current version v20040421.*

This is the data source used by ``MaxEntScan`` plugin.

Source file `fordownload`_.

.. _fordownload: http://hollywood.mit.edu/burgelab/maxent/download/fordownload.tar.gz

ClinVar
^^^^^^^

*Current version is v20201101. ClinVar is updated weekly.*

This is the data source for ClinVar to be used with ``--custom``.

.. code-block:: bash

    # Compressed VCF file
    $ curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
    # Index file
    $ curl -O ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi

SpliceAI
^^^^^^^^

*Current version is v1.3.*

This is the data source used by ``SpliceAI`` plugin.

Download requires a log in on illumina platform and `BaseSpace sequence CLI`_.

.. _BaseSpace sequence CLI: https://developer.basespace.illumina.com/docs/content/documentation/cli/cli-overview

.. code-block:: bash

    # Authenticate
    $ bs auth
    # Get id for dataset genome_scores
    $ bs list dataset
    # Download
    $ bs dataset download --id <datasetid> -o .

For annotation we are using the raw hg38 files and their index:

  - ``spliceai_scores.raw.snv.hg38.vcf.gz``
  - ``spliceai_scores.raw.snv.hg38.vcf.gz.tbi``
  - ``spliceai_scores.raw.indel.hg38.vcf.gz``
  - ``spliceai_scores.raw.indel.hg38.vcf.gz.tbi``

dbNSFP
^^^^^^

*Current version 4.1a.*

This is the data source used by ``dbNSFP`` plugin.

Source file `dbNSFP`_.

.. _dbNSFP: ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFP4.1a.zip

To create the data source:

.. code-block:: bash

    # Download and unpack
    $ wget ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFP4.1a.zip
    $ unzip dbNSFP4.1a.zip
    # Get header
    $ zcat dbNSFP4.1a_variant.chr1.gz | head -n1 > h
    # Extract information and compress to bgzip
    $ zgrep -h -v ^#chr dbNSFP4.1a_variant.chr* | sort -T /path/to/tmp_folder -k1,1 -k2,2n - | cat h - | bgzip -c > dbNSFP4.1a.gz
    # Create Tabix index
    $ tabix -s 1 -b 2 -e 2 dbNSFP4.1a.gz

gnomAD genomes
^^^^^^^^^^^^^^

*Current genome version 3.1.*

Files are available for download at https://gnomad.broadinstitute.org/downloads.

Files have been preprocessed to reduce the number of annotations using ``filter_gnomAD.py`` script inside scripts folder.
The annotations that are used and maintained are listed in ``gnomAD_3.1_fields.tsv`` file inside variants folder.

gnomAD files have been filtered while splitting by chromosomes.
The filtered VCF files have been concatenated, compressed with bgzip and indexed using Tabix.

gnomAD exomes
^^^^^^^^^^^^^

*Current exome version 2.1.1 hg38 liftover.*

The all chromosomes VCF (85.31 GiB, MD5: cff8d0cfed50adc9211d1feaed2d4ca7) was downloaded from https://gnomad.broadinstitute.org/downloads.

This file was preprocessed to reduce the number of annotations using the ``gnomAD_exome_v2_filter.py`` scripts inside the scripts folder.
The annotations that are used and maintained are listed in the ``gnomAD_2.1_fields.tsv`` file inside the variants folder.

The filtered VCF was compressed with bgzip and indexed using Tabix.

CADD
^^^^

*Current version is v1.6*

CADD SNV and indel files were downloaded from https://cadd-staging.kircherlab.bihealth.org/download

wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/whole_genome_SNVs.tsv.gz
wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/gnomad.genomes.r3.0.indel.tsv.gz

These files were supplied to the CADD plugin within VEP.


Run Vep
-------

.. code-block:: bash

    # Base command
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

    # Additional plugins
    --plugin SpliceRegion,Extended
    --plugin MaxEntScan,<PATH/fordownload>
    --plugin TSSDistance
    --plugin dbNSFP,<PATH/dbNSFP.gz>,ALL
    --plugin SpliceAI,snv=<PATH/spliceai_scores.raw.snv.hg38.vcf.gz>,indel=<PATH/spliceai_scores.raw.indel.hg38.vcf.gz>

    # Custom annotations
    --custom <PATH/clinvar.vcf.gz>,ClinVar,vcf,exact,0,ALLELEID,CLNSIG,CLNREVSTAT,CLNDN,CLNDISDB,CLNDNINCL,CLNDISDBINCL,CLNHGVS,CLNSIGCONF,CLNSIGINCL,CLNVC,CLNVCSO,CLNVI,DBVARID,GENEINFO,MC,ORIGIN,RS,SSR
    --custom <PATH/gnomAD.vcf.gz>,gnomADg,vcf,exact,0,AC,AC-XX,AC-XY,AC-afr,AC-ami,AC-amr,AC-asj,AC-eas,AC-fin,AC-mid,AC-nfe,AC-oth,AC-sas,AF,AF-XX,AF-XY,AF-afr,AF-ami,AF-amr,AF-asj,AF-eas,AF-fin,AF-mid,AF-nfe,AF-oth,AF-sas,AF_popmax,AN,AN-XX,AN-XY,AN-afr,AN-ami,AN-amr,AN-asj,AN-eas,AN-fin,AN-mid,AN-nfe,AN-oth,AN-sas,nhomalt,nhomalt-XX,nhomalt-XY,nhomalt-afr,nhomalt-ami,nhomalt-amr,nhomalt-asj,nhomalt-eas,nhomalt-fin,nhomalt-mid,nhomalt-nfe,nhomalt-oth,nhomalt-sas

Version
-------

*Current version accessed 2020-11-05.*

  - Vep: v101
  - MaxEnt: v20040421
  - ClinVar: v20201101
  - SpliceAI: v1.3
  - dbNSFP: v4.1a
  - gnomAD: v3.1

dbSNP
+++++

*Current database version is v151.*

.. code-block:: bash

    # Download all variants file from the GATK folder
    $ wget https://ftp.ncbi.nlm.nih.gov/snp/pre_build152/organisms/human_9606_b151_GRCh38p7/VCF/GATK/00-All.vcf.gz
    # Parse to reduce size
    $ python vcf_parse_keep5.py 00-All.vcf.gz 00-All_keep5.vcf
    # Compress and index
    $ bgzip 00-All_keep5.vcf
    $ bcftools index 00-All_keep5.vcf.gz
    $ tabix 00-All_keep5.vcf.gz

hg19 Liftover
+++++++++++++

This liftover (hg38 to hg19) is carried out exclusively with pyliftover (currently v0.4).  

The hg38 to hg19 chain file was supplied to pyliftover from UCSC: http://hgdownload.cse.ucsc.edu/goldenpath/hg38/liftOver/hg38ToHg19.over.chain.gz

hgvsg
+++++

*Current version 20.05*

The Human Genome Variation Society has strict guidelines and best practices for describing human genomic variants based on the reference genome, chromosomal position, and variant type. hgvsg can be used to describe all genomic variants, not just those within coding regions. The script used to generate hgvsg infomation in our pipeline implements the recommendations found here for DNA variants (http://varnomen.hgvs.org/recommendations/DNA/). We describe substitions, deletions, insertions, and deletion-insertions for all variants on the 23 nuclear chromosomes and the mitochondrial genome within this field.
