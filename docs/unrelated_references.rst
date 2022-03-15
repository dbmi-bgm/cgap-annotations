===================================
Unrelated Files and Panel of Normal
===================================

For many of the CGAP Pipelines, a collection of 20 de-identified UGRP samples are used to aid in filtering common variants. This documentation page outlines how they were created.

SNV Pipeline
------------

Coming soon...

SV Pipeline - Manta
-------------------

1. UGRP 20 Unrelated ``fastq`` files were uploaded to the (now decommissioned) cgap-wolf environment.
2. Each of the 20 samples were run through the CGAP SNV Pipeline ``v24`` ending with a final ``bam`` file following ``workflow_gatk-ApplyBQSR``.
3. Each of the resulting final ``bam`` files was run through a proband-only ``v2`` Manta workflow to produce ``vcf`` files.
4. The resulting ``vcf`` files were downloaded to a folder named ``unrelated``, which was compressed:

::

    tar -cvf unrelated.tar unrelated

5. This file was uploaded to the CGAP Portal as: ``cd647c0c-ac11-46db-9c51-bfe238e9ac13/GAPFIH794KXC.vcf.tar``

CNV Pipeline - BIC-seq2
-----------------------

1. UGRP 20 Unrelated ``fastq`` files were retrieved from Glacier Deep Archive and uploaded to the current cgap-wolf environment.
2. Each of the 20 samples were run through the ``WGS Upstream GATK Proband v27`` Metaworkflow, ending with a final ``bam`` file following ``workflow_gatk-ApplyBQSR``.
3. Each of the resulting final ``bam`` files was run through the development version of the ``CNV Germline v1`` Metaworkflow, which included only 2 steps (``workflow_BICseq2_map_norm_seg`` and ``workflow_BICseq2_vcf_convert_vcf-check``). This development version still included chromosomes X and Y as well, which have since been removed from the production ``CNV Germline v1`` Metaworkflow.
4. The resulting ``vcf`` files were downloaded to a folder named ``unrelated``, which was compressed:

::

    tar -cvf unrelated.tar unrelated

5. This file was uploaded to the CGAP Portal as: ``318788cd-661f-4327-b571-d58a9b7c301e/GAPFICPW2884.vcf.tar``

Somatic Sentieon - Panel of Normal (PON)
----------------------------------------

1. UGRP 20 Unrelated ``fastq`` files were run through the ``WGS Upstream Sentieon Proband v1`` Metaworkflow on the current cgap-wolf environment to generate 20 unrelated ``bam`` files.
2. Following `this protocol from Sentieon <https://support.sentieon.com/manual/TNscope_usage/tnscope/#generating-a-panel-of-normal-vcf-file>`_ each resulting ``bam`` file was run individually through the ``WGS Somatic Sentieon Tumor Only v1`` Metaworkflow on the current cgap-wolf environment, including the ``GAPFI4LJRN98.vcf.gz`` dbSFP file for known SNPs.
3. Continuing the protocol from above, the 20 resulting ``vcf`` output files were merged using ``bcftools`` (1.10.2).
4. This file was uploaded to the CGAP Portal as: ``833c91e9-a8cd-470e-8100-32b49ed14159/GAPFIV1QKYU9.vcf.gz``
