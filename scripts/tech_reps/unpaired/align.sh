#!/bin/bash

sizes=('5' '10' '25' '50' '100')
ns=('0' '1' '2' '3' '4')

for i in "${sizes[@]}";
do
    for j in "${ns[@]}";
    do
        qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/sim$j ../align_unpaired.pbs
        sleep 2
    done
done
