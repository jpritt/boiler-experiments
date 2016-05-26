The following commands were used to generate compressed files and results. 
Timing results were tested using the default Linux 'time' command. Peak memory results were calculated using the `testMem.py` script in the [main Boiler repository].

### Software versions

* TopHat 2 v2.1.0
* HISAT v0.1.6
* Boiler v1.0.1 (on PyPy 2.4)
* CRAMTools v3.0 (on Java v1.7)
* Goby v2.3.5 (on Java v1.7)
* Cufflinks v2.2.1
* StringTie v1.2.2
* SAMtools v0.1.19
* BEDtools v2.19.1

### Environment

Set the following environment variables:
* `BOILER_EX_HOME` should point to the directory where you have cloned this repo.
* `BOILER_HOME` should point to the directory where you have cloned the [`boiler` repo](https://github.com/jpritt/boiler).

### Running Tophat

```
tophat path/to/Bowtie2Index/genome reads1.fastq reads2.fastq
cd tophat_out
samtools view -h -o accepted_hits.sam accepted_hits.bam
```

### Running HISAT

```
hisat -x path/to/HisatIndex/genome -1 reads1.fastq -2 reads2.fastq -S hisat_out/alignments.sam
```

### Removing read names for CRAMTools

We compared Boiler's compression ratio to Goby and CRAMTools. Boiler and Goby remove read names by default, but CRAM doesn't. CRAMtools has an option `--preserve-read-names`, but we cannot find a working mechanism in version 3 to remove them.  [This CRAMTools issue](https://github.com/enasequence/cramtools/issues/48) seems to be related. For a fairer comparison, we stripped the read names before compressing.

```
$BOILER_EX_HOME/removeNames.py accepted_hits.sam accepted_hits_no_names.sam
samtools view -bS accepted_hits_no_names.sam | samtools sort - accepted_hits_no_names
samtools view -h -o accepted_hits_no_names.sam accepted_hits_no_names.bam
cd ..
```

### Running Boiler

#### Compressing TopHat alignments

```
$BOILER_HOME/boiler.py compress --frag-len-z-cutoff 0.125 --split-discordant --split-diff-strands --preprocess tophat tophat_out/accepted_hits.sam compressed/compressed.bin
```

#### Compressing HISAT alignments

```
$BOILER_HOME/boiler.py compress --frag-len-z-cutoff 0.125 --split-discordant --split-diff-strands --preprocess hisat tophat_out/accepted_hits.sam compressed/compressed.bin
```

#### Decompressing

```
$BOILER_HOME/boiler.py decompress --force-xs compressed/compressed.bin expanded.sam
```

### Assembling original transcripts

Note: use of the Cufflinks `--no-effective-length-correction` is to avoid variability due to an [issue (recently resolved)](https://github.com/cole-trapnell-lab/cufflinks/pull/32) in how Cufflinks performs effective transcript length correction.

```
mkdir -p cufflinks/orig
cufflinks --no-effective-length-correction -o cufflinks/orig tophat_out/accepted_hits.processed.bam
mkdir -p stringtie/orig
stringtie tophat_out/accepted_hits.processed.bam > stringtie/orig/transcripts.gtf
```

### Quantitating original transcripts

```
mkdir -p quant/cufflinks/orig
cufflinks -G path/to/reference.gtf --no-effective-length-correction -o quant/cufflinks/orig tophat_out/accepted_hits.processed.bam
mkdir -p quant/stringtie/orig
stringtie tophat_out/accepted_hits.processed.bam -G path/to/reference.gtf -e > quant/stringtie/orig/transcripts.gtf
```

### Assemble compressed transcripts

```
samtools view -bS expanded.sam | samtools sort - expanded
mkdir -p cufflinks/comp/
cufflinks --no-effective-length-correction -o cufflinks/comp expanded.bam
mkdir -p stringtie/comp/
stringtie expanded.bam > stringtie/comp/transcripts.gtf
```

### Quantitate compressed transcripts

```
samtools view -bS expanded.sam | samtools sort - expanded
mkdir -p quant/cufflinks/comp
cufflinks -G path/to/reference.gtf --no-effective-length-correction -o quant/cufflinks/comp expanded.bam
mkdir -p quant/stringtie/comp
stringtie expanded.bam -G path/to/reference.gtf -e > quant/stringtie/comp/transcripts.gtf
```

### Fidelity experiments

### Measuring alignment-level precision and recall

For table 5, "Precision and recall of SAM reads":

```
$BOILER_HOME/compareSAMs.py --sam1 tophat_out/accepted_hits.processed.sam --sam2 expanded.sam --out-frags results/fragments_comp.txt
```

#### Measuring non-reference-based precision and recall

Tables 8 & 9, measuring the amount of shuffling caused by Boiler compared to technical-replicate suffling.

```
$BOILER_HOME/compareGTFs.py cufflinks/orig/transcripts.gtf cufflinks/comp/transcripts.gtf
$BOILER_HOME/compareGTFs.py stringtie/orig/transcripts.gtf stringtie/comp/transcripts.gtf
```

#### Measuring isoform-level precision & recall

(Set `MODE=cufflinks` or `MODE=stringtie` as appropriate)

```
$BOILER_HOME/compareToTruth.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf
$BOILER_HOME/compareToTruth.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/comp/transcripts.gtf
```

#### WKR

In supplemental notes.  Measures weighted k-mer recall.

```
$BOILER_HOME/kc.py --refGTF ../all_reps/genes_fixed_sorted.gtf --refPRO ../all_reps/simulation.pro --sequence path/to/WholeGenomeFasta/genome.fa --assembly $MODE/orig/transcripts.gtf --data ../all_reps/simulation.fastq --kmer 15 
$BOILER_HOME/kc.py --refGTF ../all_reps/genes_fixed_sorted.gtf --refPRO ../all_reps/simulation.pro --sequence path/to/WholeGenomeFasta/genome.fa --assembly $MODE/comp/transcripts.gtf --data ../all_reps/simulation.fastq --kmer 15 
```

#### Tripartite score

Experiments described in supplemental note.  This measurement captures how closely the before- and after-compression alignment files compare to the true simulated transcriptome.

```
$BOILER_HOME/compareTripartite.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf $MODE/comp/transcripts.gtf 1
$BOILER_HOME/compareTripartite.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf $MODE/comp/transcripts.gtf 0
```

#### Comparing quantitation results

```
$BOILER_HOME/compareCufflinksQuantification.py quant/cufflinks/orig/isoforms.fpkm_tracking quant/cufflinks/comp/isoforms.fpkm_tracking
$BOILER_HOME/compareStringtieQuantification.py quant/stringtie/orig/transcripts.gtf quant/stringtie/comp/transcripts.gtf
```

### Running CRAMTools

```
java -Xmx16g -jar $CRAMTOOLS_HOME/cramtools-3.0.jar cram -I tophat_out/accepted_hits_no_names.bam -R $REFERENCE_HOME/hg19.fa -O compressed/compressed.cram
```

### Running Goby

These parameters enable the full "ACT H+T+D" approach as described in the "Goby parameter settings" section of the [Goby study](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0079871).

```
goby 16g sam-to-compact -i tophat_out/accepted_hits.bam -o compressed/compressed.goby -x MessageChunksWriter:codec=hybrid-1  -x MessageChunksWriter:template-compression=true -x AlignmentCollectionHandler:enable-domain-optimizations=true -x AlignmentWriterImpl:permutate-query-indices=false -x AlignmentCollectionHandler:ignore-read-origin=true
```

### Running BigWig

```
bedtools genomecov -bg -split -ibam accepted_hits_no_names.bam -g ChromInfo.txt > accepted_hits.bedGraph
bedGraphToBigWig accepted_hits.bedGraph ChromInfo.txt accepted_hits.bw
```

[main Boiler repository]: https://github.com/jpritt/boiler
