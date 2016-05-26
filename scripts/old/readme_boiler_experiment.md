Using boiler_experiment and boiler_eval
=======================================

I recommend these environment variables, to cut down on typing later: 

```
# TopHat                                                                                                                             
export TOPHAT_HOME=$SHARED_DIR/tophat-2.0.12.Linux_x86_64
export PATH=$PATH:$TOPHAT_HOME

# Cufflinks                                                                                                                          
export CUFFLINKS_HOME=$SHARED_DIR/cufflinks-2.2.1.Linux_x86_64
export PATH=$PATH:$CUFFLINKS_HOME

# Stringtie                                                                                                                          
export STRINGTIE_HOME=$SHARED_DIR/stringtie-1.0.3
export PATH=$PATH:$STRINGTIE_HOME

# Samtools                                                                                                                           
export SAMTOOLS_HOME=$HOME/software/samtools-0.1.18
export PATH=$PATH:$SAMTOOLS_HOME

# FeatureCounts                                                                                                                      
export SUBREAD_HOME=$SHARED_DIR/subread-1.4.6-p3-Linux-x86_64
export PATH=$PATH:$SUBREAD_HOME/bin

# Pypy                                                                                                                               
export PYPY_HOME=$SHARED_DIR/pypy3-2.4-linux_x86_64-portable
export PATH=$PATH:$PYPY_HOME/bin
```

### Paired-end

From the `compress-alignments` directory, run something like this (substituting for `IN`, `OUTPUT`, and `NTHREADS`):

```
IN=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/paired/sim1000000
OUT=$HOME/compress-alignments-test/paired/sim1000000
NTHREADS=12
SHARED_DIR=/scratch0/langmead-fs1/shared
mkdir -p $OUT
python scripts/boiler_experiment.py \
    --gtf $IN/genes_fixed_sorted.gtf \
    --pro $IN/simulation.pro \
    --output $OUT \
    --bt2-index $SHARED_DIR/igenomes/Drosophila_melanogaster/Ensembl/BDGP5/Sequence/Bowtie2Index/genome \
    --m1 $IN/simulation_1.fastq \
    --m2 $IN/simulation_2.fastq \
    --compress boiler.py \
    --python3-exe $PYPY_HOME/bin/pypy3 \
    --num-threads $NTHREADS \
    --tophat \
    --cufflinks \
    --stringtie \
    --featurecounts
```

### Unpaired

From the `compress-alignments` directory, run something like this (substituting for `IN`, `OUTPUT`, and `NTHREADS`):

```
IN=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/single/sim1000000
OUT=$HOME/compress-alignments-test/single/sim1000000
NTHREADS=12
SHARED_DIR=/scratch0/langmead-fs1/shared
mkdir -p $OUT
python scripts/boiler_experiment.py \
    --gtf $IN/genes_fixed_sorted.gtf \
    --pro $IN/simulation.pro \
    --output $OUT \
    --bt2-index $SHARED_DIR/igenomes/Drosophila_melanogaster/Ensembl/BDGP5/Sequence/Bowtie2Index/genome \
    --unpaired $IN/simulation.fastq \
    --compress boiler.py \
    --python3-exe $PYPY_HOME/bin/pypy3 \
    --num-threads $NTHREADS \
    --tophat \
    --cufflinks \
    --stringtie \
    --featurecounts
```

### Results

Results are now in subdirectories of `$OUT`.  (Also, the input GTF and PRO files have been copied there.  The reference genome and the input reads have not been copied, but perhaps should.  They would be helpful for running `kc.py`.)  Here's what some of the directory structure looks like for an unpaired experiment:

```
$ tree $HOME/compress-alignments-test/paired/sim1000000 | head -20
/home/langmead/compress-alignments-test/paired/sim1000000
|-- cufflinks_tophat
|   |-- compressed
|   |   |-- cufflinks_version.txt
|   |   |-- genes.fpkm_tracking
|   |   |-- isoforms.fpkm_tracking
|   |   |-- skipped.gtf
|   |   `-- transcripts.gtf
|   `-- uncompressed
|       |-- cufflinks_version.txt
|       |-- genes.fpkm_tracking
|       |-- isoforms.fpkm_tracking
|       |-- skipped.gtf
|       `-- transcripts.gtf
|-- featurecounts_tophat
|   |-- compressed
|   |   |-- counts_exon.tsv
|   |   |-- counts_exon.tsv.summary
|   |   |-- counts_gene.tsv
|   |   |-- counts_gene.tsv.summary
```

To evaluate the results, assuming we're still in the `compress-alignments` directory and `OUT` is still defined:

```
python scripts/boiler_eval.py \
    --input $OUT \
    --boiler-dir=. \
    --python3-exe $PYPY_HOME/bin/pypy3
```

The results have been added to the directory structure of `$OUT`:

```
$ tree $HOME/compress-alignments-test/sim1000000 | head -20
/home/langmead/compress-alignments-test/sim1000000
|-- cufflinks_tophat
|   |-- compressed
|   |   |-- compare_to_truth.txt
|   |   |-- cufflinks_version.txt
|   |   |-- genes.fpkm_tracking
|   |   |-- isoforms.fpkm_tracking
|   |   |-- skipped.gtf
|   |   `-- transcripts.gtf
|   |-- tripartite_nonstrict.txt
|   |-- tripartite_strict.txt
|   `-- uncompressed
|       |-- compare_to_truth.txt
|       |-- cufflinks_version.txt
|       |-- genes.fpkm_tracking
|       |-- isoforms.fpkm_tracking
|       |-- skipped.gtf
|       `-- transcripts.gtf
|-- featurecounts_tophat
|   |-- compressed
```

### featureCounts plots

If you're trying to diagnose compressed/uncompressed differences, the isoform assembly and quantitation results can be frustratingly hard to interpret.  A nice, easy-to-interpret plot is a scatter plot showing how many reads (or fragments, in the case of paired-end) overlap annotated genes in the uncompressed versus compressed outputs.  The `featureCounts` tool compiles these counts as part of the `boiler-experiment.py` script (if you specify `--featurecounts`).  To make this plot, change to the `$OUT/featurecounts_tophat` directory and run `Rscript /path/to/compress-alignments/scripts/featurecount_plot.R`:

```
$ cd $OUT/featurecounts_tophat
$ tree
.
|-- compressed
|   |-- counts_exon.tsv
|   |-- counts_exon.tsv.summary
|   |-- counts_gene.tsv
|   |-- counts_gene.tsv.summary
|   `-- featurecounts_version.txt
`-- uncompressed
    |-- counts_exon.tsv
    |-- counts_exon.tsv.summary
    |-- counts_gene.tsv
    |-- counts_gene.tsv.summary
    `-- featurecounts_version.txt

2 directories, 10 files
$ Rscript $FS1_HOME/git/compress-alignments/scripts/featurecount_plot.R
null device 
          1 
null device 
          1 
$ tree
$ ls -l
total 1244
drwxrwxr-x 2 langmead langmead    4096 May 18 09:59 compressed
-rw-rw-r-- 1 langmead langmead 1043708 May 18 10:07 exon.pdf
-rw-rw-r-- 1 langmead langmead  219514 May 18 10:07 gene.pdf
drwxrwxr-x 2 langmead langmead    4096 May 18 09:59 uncompressed
```

Take a look at `gene.pdf`.
