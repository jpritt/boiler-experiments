#!/bin/bash

#folders=('HG00100', 'HG00101', 'HG00102', 'HG00103', 'HG00104')
folders=('HG00100')

for i in "${folders[@]}";
do
    qsub -vDIR=/scratch0/langmead-fs1/user/jacob/compress-alignments-test/human/$i,ALIGNMENTS=${i}_accepted_hits time.pbs
done
