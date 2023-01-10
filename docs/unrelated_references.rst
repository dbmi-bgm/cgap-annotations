===================================
Unrelated Files and Panel of Normal
===================================

For many of the CGAP Pipelines, a collection of 20 de-identified UGRP samples are used to aid in filtering common variants. This documentation page outlines how they were created.

SNV Pipeline - Unrelated RCK files
----------------------------------

Sentieon
++++++++

1. 20 unrelated ``fastq`` files from UGRP dataset were run through the Upstream Sentieon module (v1.0.0) to generate analysis-ready ``bam`` files.
2. The ``bam`` files were then processed using a custom module (SNV Unrelated, v1.0.0) that executes granite ``mpileupCounts`` and ``rckTar`` commands.
3. The final file was uploaded to the CGAP Portal as: ``196ef586-be28-40c5-a244-d739fd173984/GAPFIMO8Y4K1.vcf.gz``

GATK
++++

1. 20 unrelated ``fastq`` files from UGRP dataset were run through the Upstream GATK module (v1.0.0) to generate analysis-ready ``bam`` files.
2. The ``bam`` files were then processed using a custom module (SNV Unrelated, v1.0.0) that executes granite ``mpileupCounts`` and ``rckTar`` commands.
3. The final file was uploaded to the CGAP Portal as: ``eac862c0-8c87-4838-83cb-9a77412bff6f/GAPFIMO8Y4PZ.vcf.gz``


Somatic Sentieon - Panel of Normal (PON)
----------------------------------------

1. 20 unrelated ``fastq`` files from UGRP dataset were run through the Upstream Sentieon module (v1.0.0) to generate analysis-ready ``bam`` files.
2. Following `this protocol from Sentieon <https://support.sentieon.com/manual/TNscope_usage/tnscope/#generating-a-panel-of-normal-vcf-file>`_ each resulting ``bam`` file was run individually through the Somatic Sentieon Tumor Only module (v1.0.0), using ``GAPFI4LJRN98.vcf.gz`` dbSNP file for known SNPs.
3. The 20 resulting ``vcf`` output files were merged using BCFtools (1.10.2).
4. This file was uploaded to the CGAP Portal as: ``833c91e9-a8cd-470e-8100-32b49ed14159/GAPFIV1QKYU9.vcf.gz``


SV Pipeline - Manta
-------------------

1. UGRP 20 Unrelated ``fastq`` files were uploaded to the (now decommissioned) cgap-wolf environment.
2. Each of the 20 samples were run through the Upstream GATK module (v24), ending with a final ``bam`` file following ``workflow_gatk-ApplyBQSR``.
3. Each of the resulting final ``bam`` files was run through a proband-only Manta workflow (v2) to produce ``vcf`` files.
4. The resulting ``vcf`` files were downloaded to a folder named ``unrelated``, which was compressed:

.. code-block:: bash

    tar -cvf unrelated.tar unrelated

5. This file was uploaded to the CGAP Portal as: ``cd647c0c-ac11-46db-9c51-bfe238e9ac13/GAPFIH794KXC.vcf.tar``


CNV Pipeline - BICseq2
----------------------

1. UGRP 20 Unrelated ``fastq`` files were retrieved from Glacier Deep Archive and uploaded to the current cgap-wolf environment.
2. Each of the 20 samples were run through the Upstream GATK module (v27), ending with a final ``bam`` file following ``workflow_gatk-ApplyBQSR``.
3. Each of the resulting final ``bam`` files was run through the development version of the CNV module (v1), which included only 2 steps (``workflow_BICseq2_map_norm_seg`` and ``workflow_BICseq2_vcf_convert_vcf-check``). This development version still included chromosomes X and Y as well, which have since been removed from the production version.
4. The resulting ``vcf`` files were downloaded to a folder named ``unrelated``, which was compressed:

.. code-block:: bash

    tar -cvf unrelated.tar unrelated

5. This file was uploaded to the CGAP Portal as: ``318788cd-661f-4327-b571-d58a9b7c301e/GAPFICPW2884.vcf.tar``
