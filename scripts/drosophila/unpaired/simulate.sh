#!/bin/bash

sizes=('5' '10' '25' '50' '100')

for i in "${sizes[@]}";
do
    mkdir -p /scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/all_reps
    cp simulation$i.par /scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/all_reps/simulation.par
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/all_reps ../simulate_unpaired.pbs
    sleep 2
done
