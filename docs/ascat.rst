===============
ASCAT Resources
===============

*Current software version is 3.0.0.*

Source files for `Software`_ .

.. _Software: https://github.com/VanLoo-lab/ascat

ASCAT requires a set of external reference data that are provided as additional data sources in the main repository of the software, `here <https://github.com/VanLoo-lab/ascat/tree/master/ReferenceFiles/WGS>`__. For convenience, we collected and packaged these resources into a single ``tar`` archive that contains the following set of files.

Loci Files
^^^^^^^^^^
*ASCAT repository commit 7fc8c9d, files version 20092021*

Loci files contain SNP positions derived from the 1000Genomes prepared for **hg38/GRCh38**, available `here <https://www.dropbox.com/s/80cq0qgao8l1inj/G1000_loci_hg38.zip>`__.
We operate on chr-based ``bam`` files, so the original loci files were modified and the ``chr-`` prefix was added by running the command:

.. code-block:: bash

    for i in {1..22} X; do sed -i 's/^/chr/' G1000_loci_hg38_chr${i}.txt; done

Allele Files
^^^^^^^^^^^^
*ASCAT repository commit 7fc8c9d, files version 20092021*

Allele files contain SNP positions with their reference and alternative nucleotide bases based on the 1000Genomes prepared for **hg38/GRCh38**, available `here <https://www.dropbox.com/s/uouszfktzgoqfy7/G1000_alleles_hg38.zip>`__.

GC Correction File
^^^^^^^^^^^^^^^^^^
*ASCAT repository commit 7fc8c9d, files version 20092021*

The GC correction file contains the GC content around every SNP for increasing window sizes, available `here <https://www.dropbox.com/s/n7g5dh0ld1hcto8/GC_G1000_hg38.zip>`__.
