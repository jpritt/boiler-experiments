#!/bin/bash

sizes=('5' '10' '25' '50' '100')

for i in "${sizes[@]}";
do
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i,MODE=cufflinks,TRUTH_GTF=/scratch0/langmead-fs1/user/jacob/genomes/Drosophila_melanogaster/Ensembl/BDGP5/Annotation/Genes/genes_fixed.gtf ../compute_accuracy.pbs
    sleep 2
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i,MODE=stringtie,TRUTH_GTF=/scratch0/langmead-fs1/user/jacob/genomes/Drosophila_melanogaster/Ensembl/BDGP5/Annotation/Genes/genes_fixed.gtf ../compute_accuracy.pbs
    sleep 2
done
