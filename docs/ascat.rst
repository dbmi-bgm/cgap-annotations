============
Data Sources
============

Data sources for ASCAT.

ASCAT
+++++

*Current software version is 3.0.0.*

Source files for `Software`_ .

.. _Software: https://github.com/VanLoo-lab/ascat

ASCAT requires input files that are reused in each run. All the data are stored in a single `tar` file, which includes: 

Loci files
^^^^^^^^^^

Loci files contain SNP positions derived from the 1000Genomes prepared for GRCh38, available `here <https://www.dropbox.com/s/80cq0qgao8l1inj/G1000_loci_hg38.zip>`__ (version 20092021) .
We operate on chr-based BAM files, so the original loci files were modified and the chr- prefix was added by running the command: 

`for i in {1..22} X; do sed -i 's/^/chr/' G1000_loci_hg38_chr${i}.txt; done`


Alleles files
^^^^^^^^^^^^^

Alleles files contain SNP positions with their reference and alternative nucletide bases based on the 1000Genomes prepared for GRCh38, available `here <https://www.dropbox.com/s/uouszfktzgoqfy7/G1000_alleles_hg38.zip>`__ (version 20092021). 

GC Correction file
^^^^^^^^^^^^^^^^^^

The GC correction file contains the GC content around every SNP for increasing window sizes, available `here <https://www.dropbox.com/s/n7g5dh0ld1hcto8/GC_G1000_hg38.zip>`__ (version 20092021).  
