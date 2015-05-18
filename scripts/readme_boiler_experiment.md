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

From the `compress-alignments` directory, run something like this (substituting for `INPUT`, `OUTPUT`, and `NTHREADS`):

```
IN=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/paired/sim1000000
OUT=$HOME/compress-alignments-test/sim1000000
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

Results are now in subdirectories of `$OUT`.  (Also, the input GTF and PRO files have been copied there.  The reference genome and the input reads have not been copied, but perhaps should.  They would be helpful for running `kc.py`.) 

```
[langmead@login compress-alignments-test]$ tree ~/compress-alignments-test/sim1000000 | head -20
/home/langmead/compress-alignments-test/sim1000000
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
[langmead@login compress-alignments]$ tree ~/compress-alignments-test/sim1000000 | head -20
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