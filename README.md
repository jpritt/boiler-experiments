The following commands were used to generate compressed files and results. 
Timing results were tested using the default Linux 'time' command. Peak memory results were calculated using the `testMem.py` script in the [main Boiler repository].

##### Tophat #####

```
tophat path/to/Bowtie2Index/genome reads1.fastq reads2.fastq
cd tophat_out
samtools view -h -o accepted_hits.sam accepted_hits.bam
```

# Add any inferred strand tags in pairs

The `inferXStags.py` script is in the [main Boiler repository].

```
inferXStags.py accepted_hits.sam > accepted_hits_fixed.sam
samtools view -bS accepted_hits_fixed.sam | samtools sort - accepted_hits_fixed
samtools view -h -o accepted_hits_fixed.sam accepted_hits_fixed.bam
```

# Remove read names for CRAMTools

```
removeNames.py accepted_hits_fixed.sam accepted_hits_no_names.sam
samtools view -bS accepted_hits_no_names.sam | samtools sort - accepted_hits_no_names
samtools view -h -o accepted_hits_no_names.sam accepted_hits_no_names.bam
cd ../
```

# Assemble original transcripts
mkdir -p cufflinks/orig
cufflinks --no-effective-length-correction -o cufflinks/orig tophat_out/accepted_hits_fixed.bam
mkdir -p stringtie/orig
stringtie tophat_out/accepted_hits_fixed.bam > stringtie/orig/transcripts.gtf

##### Boiler #####
./boiler.py compress --frag-len-z-cutoff 0.125 --split-discordant --split-diff-strands tophat_out/accepted_hits_fixed.sam compressed/compressed.bin
./boiler.py decompress --force-xs compressed/compressed.bin expanded.sam

# Assemble compressed transcripts
samtools view -bS expanded.sam | samtools sort - expanded
mkdir -p cufflinks/comp/
cufflinks --no-effective-length-correction -o cufflinks/comp expanded.bam
mkdir -p stringtie/comp/
stringtie expanded.bam > stringtie/comp/transcripts.gtf

# Results direct comparison
path/to/boiler/compareSAMs.py --sam1 tophat_out/accepted_hits_fixed.sam --sam2 expanded.sam --out-frags results/fragments_comp.txt
path/to/boiler/compareGTFs.py cufflinks/orig/transcripts.gtf cufflinks/comp/transcripts.gtf
path/to/boiler/compareGTFs.py stringtie/orig/transcripts.gtf stringtie/comp/transcripts.gtf

# Results comparison to reference
# $MODE = cufflinks | stringtie

# Precision & Recall
path/to/boiler/compareToTruth.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf
path/to/boiler/compareToTruth.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/comp/transcripts.gtf

# WKR
path/to/boiler/kc.py --refGTF ../all_reps/genes_fixed_sorted.gtf --refPRO ../all_reps/simulation.pro --sequence path/to/WholeGenomeFasta/genome.fa --assembly $MODE/orig/transcripts.gtf --data ../all_reps/simulation.fastq --kmer 15 
path/to/boiler/kc.py --refGTF ../all_reps/genes_fixed_sorted.gtf --refPRO ../all_reps/simulation.pro --sequence path/to/WholeGenomeFasta/genome.fa --assembly $MODE/comp/transcripts.gtf --data ../all_reps/simulation.fastq --kmer 15 

# Tripartite score
path/to/boiler/compareTripartite.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf $MODE/comp/transcripts.gtf 1
path/to/boiler/compareTripartite.py ../all_reps/simulation.pro ../all_reps/genes_fixed_sorted.gtf $MODE/orig/transcripts.gtf $MODE/comp/transcripts.gtf 0

##### CRAMTools #####
java -Xmx16g -jar /scratch0/langmead-fs1/shared/cramtools/cramtools-3.0.jar cram -I tophat_out/accepted_hits_no_names.bam -R /scratch0/langmead-fs1/shared/references/hg19/fasta/hg19.fa -O compressed/compressed.cram

##### Goby #####
goby 16g sam-to-compact -i tophat_out/accepted_hits.bam -o compressed/compressed.goby -x MessageChunksWriter:codec=hybrid-1  -x MessageChunksWriter:template-compression=true -x AlignmentCollectionHandler:enable-domain-optimizations=true -x AlignmentWriterImpl:permutate-query-indices=false -x AlignmentCollectionHandler:ignore-read-origin=true

[main Boiler repository]: https://github.com/jpritt/boiler
