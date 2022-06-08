=========================
BIC-seq2 Mappability File
=========================

``BIC-seq2 Norm`` makes use of a unique mappability file to aid in the process of normalizing the raw coverage data presented in the ``seq`` files. This mappability file must be generated for each library size (e.g., 150 bp) given that unique mappability will vary with read length. A 100 bp read might not map uniquely at a given position, but a 150 bp read starting from the same position might map uniquely given 50 additional bases at the end.

The current mappability file was generated for 150 bp reads using a custom workflow, as follows:

1. The file ``chromosomes.txt`` was created with only the 23 chromosomes from **hg38** (e.g., chr1, chr2 ... chr22, chrX, chrY; each on their own line). These regions were extracted from our **hg38** reference genome ``GAPFIXRDPDK5.fa`` to generate ``hg38_main_chrs.fa`` and a ``fasta`` index file was generated for this output.

::

    for file in $(cat chromosomes.txt); do samtools faidx GAPFIXRDPDK5.fa $file >> hg38_main_chrs.fa; done
    samtools faidx hg38_main_chrs.fa

2. Using an archived version of ``gemtools`` (v 1.7.1-i3) distributed in the github repo below, the initial mappability file was generated and converted to ``wig`` format:

::

    git clone https://github.com/LinjieWu/GenerateMappability
    cd GenerateMappability
    python setup.py
    cd ..

    SoftwareDir="<path_to_folder>/GenerateMappability"
    export PATH=${SoftwareDir}/gemtools-1.7.1-i3/bin/:$PATH

    gem-indexer -T 16 -c dna -i hg38_main_chrs.fa -o hg38_main_chr_index

    gem-mappability -T 16 -I hg38_main_chr_index.gem -l 150 -o hg38_full_mappability_150

    gem-2-wig -I hg38_main_chr_index.gem -i hg38_full_mappability_150.mappability -o hg38_full_mappability_150

3. This ``wig`` mappability file must next be converted to a ``bed`` file through a series of conversion steps using tools available from `UCSC <http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64.v385/>`_:

::

    ./wigToBigWig hg38_full_mappability_150.wig hg38_full_mappability_150.sizes hg38_full_mappability_150.bw

    ./bigWigToBedGraph hg38_full_mappability_150.bw  hg38_full_mappability_150.bedGraph

    ./bedGraphTobed hg38_full_mappability_150.bedGraph hg38_full_mappability_150.bed 1

4. After testing this mappability file, we determined that repetitive regions at the centromeres were causing large numbers of artefactual CNVs. ``BIC-seq2`` had been optimized previously for **hg19** with mappability files that excluded the centromeres, so we decided to also exclude the centromeric regions from our **hg38** mappability file. The centromeres for **hg38** were pulled from UCSC as follows:

  1. Navigate to http://genome.ucsc.edu/cgi-bin/hgTables
  2. Under "assembly", select "Dec. 2013 (GRCh38/hg38)"
  3. Under "group", select "Mapping and Sequencing"
  4. Under "track", select "Chromosome Band (Ideogram)"
  5. Under "filter", select "create"
  6. Under "gieStain", select "does" match, and type "acen" in the text box, then select "submit"
  7. Under "output format", select "BED - browser extensible data"
  8. Select "get output"
  9. Select "get BED"


5. This ``bed`` file was saved as ``centromeres.txt`` and subtracted from the existing mappability file:

::

    bedtools subtract -a hg38_full_mappability_150.bed -b centromeres.bed > hg38_full_mappability_150_no_centromeres.bed

6. Finally, the ``bed`` file was parsed to generate a single mappability file for each chromosome in the format required by ``BIC-seq2 Norm``:

::

    for file in $(cat chromosomes.txt); do echo $file; grep -P ${file}'\t' hg38_full_mappability_150_no_centromeres.bed | awk -v OFS='\t' '{print $2, $3}' > full_mappability_hg38_150_no_centromeres/${file}_mappability; done
