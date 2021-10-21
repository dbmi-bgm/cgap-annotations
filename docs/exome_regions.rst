===================================
Generation of the exome region file
===================================

Data sources and code used to generate the exome region file used by HaplotyeCaller in WES runs

Current version
+++++++++++++++

*Accessed 2021-10-21.*

VEP v101
--------

VEP v101 `archive`_ website:

.. _archive: http://aug2020.archive.ensembl.org/Homo_sapiens/Info/Index?db=core


VEP v101 `gtf`_ file :

.. _gtf: ftp://ftp.ensembl.org/pub/release-101/gtf/homo_sapiens/

  - Homo_sapiens.GRCh38.101.gtf.gz


Reference file creation
-----------------------

To transform this VEP ``gtf`` file into a comprehensive ``bed`` file of all possible transcripts and UTR regions, one python script and two ``bedtools`` (v2.30.0) commands were used.

::

    bgzip -d Homo_sapiens.GRCh38.101.gtf.gz

    python exome_hg38_region_of_interest.py Homo_sapiens.GRCh38.101.gtf regions_bed_final.bed

    bedtools sort -i regions_bed_final.bed > sort_regions_bed_final.bed

    bedtools merge -i sort_regions_bed_final.bed > merge_sort_regions_bed_final.bed

``exome_hg38_region_of_interest.py`` is available in this repository in ``/genes/exome_regions/``
