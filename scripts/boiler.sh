# Run Boiler (compress/decompress), then run cufflinks on the resulting SAM file
../../../compress-alignments/boiler.py --alignments tophat_out/accepted_hits.sam --binary
samtools view -bS expanded.sam | samtools sort - expanded
cufflinks expanded.bam 

