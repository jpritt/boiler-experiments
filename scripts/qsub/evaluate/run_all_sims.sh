#!/bin/bash

folders=('single/sim500000' 'single/sim1000000', 'single/sim2500000', 'single/sim5000000', 'single/sim10000000', 'paired/sim500000', 'paired/sim1000000', 'paired/sim2500000', 'paired/sim5000000', 'paired/sim10000000')

for i in "${folders[@]}";
do
    mkdir -p /scratch0/langmead-fs1/user/jacob/compress-alignments-test/$i/results
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/$i,ALIGNMENTS=tophat_out/accepted_hits eval_no_ref.pbs > /scratch0/langmead-fs1/user/jacob/compress-alignments-test/$i/results/results.txt
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/$i,ALIGNMENTS=tophat_out/accepted_hits eval_with_ref.pbs >> /scratch0/langmead-fs1/user/jacob/compress-alignments-test/$i/results/results.txt
done