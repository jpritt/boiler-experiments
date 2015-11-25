#!/bin/bash

sizes=('5' '10' '25' '50' '100')
ns=('0')
#ns=('0' '1' '2' '3' '4')

for i in "${sizes[@]}";
do
    for j in "${ns[@]}";
    do
        qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/sim$j ../eval_no_ref.pbs
        sleep 1
        qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/drosophila/tech_reps/single$i/sim$j ../eval_with_ref.pbs
        sleep 1
    done
done
