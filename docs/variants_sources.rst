============
Data Sources
============

Software and data sources for variants annotation.

VEP
+++

*Current software version is 101.*

Annotation uses Variant Effect Predictor (VEP) software.

Source files for `Software`_ and `Plugins`_.

.. _Software: https://github.com/Ensembl/ensembl-vep/tree/release/101
.. _Plugins: https://github.com/Ensembl/VEP_plugins/tree/release/101

Annotation Sources
------------------

VEP
^^^

This is the main annotation source for VEP.

Source file `v101`_ for homo_sapiens on **hg38/GRCh38**.

.. _v101: ftp://ftp.ensembl.org/pub/release-101/variation/vep/homo_sapiens_vep_101_GRCh38.tar.gz

.. code-block:: bash

    $ wget ftp://ftp.ensembl.org/pub/release-101/variation/vep/homo_sapiens_vep_101_GRCh38.tar.gz

MaxEnt
^^^^^^

*Current version v20040421.*

This is the data source used by MaxEntScan plugin.

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

This is the data source used by SpliceAI plugin.

Download requires a log in on illumina platform and `BaseSpace sequence CLI`_.

.. _BaseSpace sequence CLI: https://developer.basespace.illumina.com/docs/content/documentation/cli/cli-overview

.. code-block:: bash

    # Authenticate
    $ bs auth
    # Get id for dataset genome_scores
    $ bs list dataset
    # Download
    $ bs dataset download --id <datasetid> -o .

For annotation we are using the raw **hg38/GRCh38** files and their index:

  - ``spliceai_scores.raw.snv.hg38.vcf.gz``
  - ``spliceai_scores.raw.snv.hg38.vcf.gz.tbi``
  - ``spliceai_scores.raw.indel.hg38.vcf.gz``
  - ``spliceai_scores.raw.indel.hg38.vcf.gz.tbi``

dbNSFP
^^^^^^

*Current version 4.1a.*

This is the data source used by dbNSFP plugin.

A small modification was made to the source code for the dbNSFP plugin to allow for annotation of non-missense variants. The change is shown below with the original code commented out.

.. code-block:: perl

  #my %INCLUDE_SO = map {$_ => 1} qw(missense_variant stop_lost stop_gained start_lost);
  my %INCLUDE_SO = map {$_ => 1} qw(missense_variant stop_lost stop_gained start_lost splice_donor_variant splice_acceptor_variant splice_region_variant frameshift inframe_insertion inframe_deletion);

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
    # Create tabix index
    $ tabix -s 1 -b 2 -e 2 dbNSFP4.1a.gz

gnomAD Genomes
^^^^^^^^^^^^^^

*Current genome version 3.1.*

Files are available for download at https://gnomad.broadinstitute.org/downloads.

Files have been preprocessed to reduce the number of annotations using ``filter_gnomAD.py`` script inside scripts folder.
The annotations that are used and maintained are listed in ``gnomAD_3.1_fields.tsv`` file inside variants folder.

gnomAD files have been filtered while splitting by chromosomes.
The filtered ``vcf`` files have been concatenated, compressed with ``bgzip`` and indexed using ``tabix``.

gnomAD Exomes
^^^^^^^^^^^^^

*Current exome version 2.1.1 hg38/GRCh38 lift-over.*

The all chromosomes ``vcf`` (85.31 GiB, MD5: cff8d0cfed50adc9211d1feaed2d4ca7) was downloaded from https://gnomad.broadinstitute.org/downloads.

This file was preprocessed to reduce the number of annotations using the ``gnomAD_exome_v2_filter.py`` scripts inside the scripts folder.
The annotations that are used and maintained are listed in the ``gnomAD_2.1_fields.tsv`` file inside the variants folder.

The filtered ``vcf`` was compressed with ``bgzip`` and indexed using ``tabix``.

gnomAD Structural Variants (hg38/GRCh38 lift-over)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Current SV version is nstd166 hg38/GRCh38 lift-over.*

File was originally downloaded (here: https://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_study/vcf/nstd166.GRCh38.variant_call.vcf.gz), but that same link now takes you to a newer and incorrect file.

See ``nstd166_GRCh38_readme.txt`` in the ``s3://cgap-annotations/gnomAD/SV/`` for in-depth explanation. We have copies of both the original (currently used) and the newer file in the bucket.

CADD
^^^^

*Current version is v1.6*

CADD SNV and INDEL files were downloaded from https://cadd-staging.kircherlab.bihealth.org/download

.. code-block:: bash

    $ wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/whole_genome_SNVs.tsv.gz
    $ wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/gnomad.genomes.r3.0.indel.tsv.gz

These files were supplied to the CADD plugin within VEP.

Conservation Scores
^^^^^^^^^^^^^^^^^^^

*Current version is UCSC hg38/GRCh38 for phyloP30way, phyloP100way, and phastCons100way*

.. code-block:: bash

    $ wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phyloP30way/hg38.phyloP30way.bw
    $ wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phyloP100way/hg38.phyloP100way.bw
    $ wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phastCons100way/hg38.phastCons100way.bw

These files were supplied to customs within VEP.

Run VEP
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
    --plugin dbNSFP,<PATH/dbNSFP.gz>,phyloP100way_vertebrate_rankscore,GERP++_RS,GERP++_RS_rankscore,SiPhy_29way_logOdds,SiPhy_29way_pi,PrimateAI_score,PrimateAI_pred,PrimateAI_rankscore,CADD_raw_rankscore,Polyphen2_HVAR_pred,Polyphen2_HVAR_rankscore,Polyphen2_HVAR_score,SIFT_pred,SIFT_converted_rankscore,SIFT_score,REVEL_rankscore,REVEL_score,Ensembl_geneid,Ensembl_proteinid,Ensembl_transcriptid
    --plugin SpliceAI,snv=<PATH/spliceai_scores.raw.snv.hg38.vcf.gz>,indel=<PATH/spliceai_scores.raw.indel.hg38.vcf.gz>
    --plugin CADD,<PATH/whole_genome_SNVs.tsv.gz>,<PATH/gnomad.genomes.r3.0.indel.tsv.gz>

    # Custom annotations
    --custom <PATH/clinvar.vcf.gz>,ClinVar,vcf,exact,0,ALLELEID,CLNSIG,CLNREVSTAT,CLNDN,CLNDISDB,CLNDNINCL,CLNDISDBINCL,CLNHGVS,CLNSIGCONF,CLNSIGINCL,CLNVC,CLNVCSO,CLNVI,DBVARID,GENEINFO,MC,ORIGIN,RS,SSR
    --custom <PATH/gnomAD.vcf.gz>,gnomADg,vcf,exact,0,AC,AC-XX,AC-XY,AC-afr,AC-ami,AC-amr,AC-asj,AC-eas,AC-fin,AC-mid,AC-nfe,AC-oth,AC-sas,AF,AF-XX,AF-XY,AF-afr,AF-ami,AF-amr,AF-asj,AF-eas,AF-fin,AF-mid,AF-nfe,AF-oth,AF-sas,AF_popmax,AN,AN-XX,AN-XY,AN-afr,AN-ami,AN-amr,AN-asj,AN-eas,AN-fin,AN-mid,AN-nfe,AN-oth,AN-sas,nhomalt,nhomalt-XX,nhomalt-XY,nhomalt-afr,nhomalt-ami,nhomalt-amr,nhomalt-asj,nhomalt-eas,nhomalt-fin,nhomalt-mid,nhomalt-nfe,nhomalt-oth,nhomalt-sas
    --custom <PATH/trimmed_gnomad.exomes.r2.1.1.sites.liftover_grch38.vcf.gz>,gnomADe2,vcf,exact,0,AC,AN,AF,nhomalt,AC_oth,AN_oth,AF_oth,nhomalt_oth,AC_sas,AN_sas,AF_sas,nhomalt_sas,AC_fin,AN_fin,AF_fin,nhomalt_fin,AC_eas,AN_eas,AF_eas,nhomalt_eas,AC_amr,AN_amr,AF_amr,nhomalt_amr,AC_afr,AN_afr,AF_afr,nhomalt_afr,AC_asj,AN_asj,AF_asj,nhomalt_asj,AC_nfe,AN_nfe,AF_nfe,nhomalt_nfe,AC_female,AN_female,AF_female,nhomalt_female,AC_male,AN_male,AF_male,nhomalt_male,AF_popmax
    --custom <PATH/hg38.phyloP100way.bw>,phylop100verts,bigwig,exact,0
    --custom <PATH/hg38.phyloP30way.bw>,phylop30mams,bigwig,exact,0
    --custom <PATH/hg38.phastCons100way.bw>,phastcons100verts,bigwig,exact,0

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

hg38/GRCh38 to hg19/GRCh37 lift-over (pyliftover)
+++++++++++++++++++++++++++++++++++++++++++++++++

This lift-over (**hg38/GRCh38** to **hg19/GRCh37**) is carried out exclusively with pyliftover (currently v0.4).

The **hg38/GRCh38** to **hg19/GRCh37** chain file was supplied to pyliftover from UCSC: http://hgdownload.cse.ucsc.edu/goldenpath/hg38/liftOver/hg38ToHg19.over.chain.gz.

Cytoband
++++++++

The **hg38/GRCh38** Cytoband reference file from UCSC (http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cytoBand.txt.gz).

HGVSg
+++++

*Current version 20.05*

The Human Genome Variation Society has strict guidelines and best practices for describing human genomic variants based on the reference genome, chromosomal position, and variant type. HGVSg can be used to describe all genomic variants, not just those within coding regions. The script used to generate HGVSg infomation in our pipeline implements the recommendations found here for DNA variants (http://varnomen.hgvs.org/recommendations/DNA/). We describe substitions, deletions, insertions, and deletion-insertions for all variants on the 23 nuclear chromosomes and the mitochondrial genome within this field.

Version
+++++++

*Current version accessed 2021-04-20.*

  - VEP: v101
  - MaxEnt: v20040421
  - ClinVar: v20201101
  - SpliceAI: v1.3
  - dbNSFP: v4.1a
  - gnomAD: v3.1
  - gnomAD_exomes: v2.1.1
  - CADD: v1.6
  - phyloP30way: hg38/GRCh38
  - phyloP100way: hg38/GRCh38
  - phastCons100way: hg38/GRCh38
  - dbSNP: v151
  - HGVSg: 20.05
  - Cytoband: hg38/GRCh38
