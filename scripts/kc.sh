# Compute KC score of original and compressed cufflinks results
echo 'Original:'
../../../compress-alignments/kc.py --refGTF genes_fixed_sorted.gtf --refPRO simulation.pro --sequence ../../../genomes/Drosophila_melanogaster/Ensembl/BDGP5/Sequence/WholeGenomeFasta/genome.fa --assembly cufflinks/transcripts.gtf --data simulation.fastq --kmer 15

echo ''
echo 'Compressed:'
../../../compress-alignments/kc.py --refGTF genes_fixed_sorted.gtf --refPRO simulation.pro --sequence ../../../genomes/Drosophila_melanogaster/Ensembl/BDGP5/Sequence/WholeGenomeFasta/genome.fa --assembly transcripts.gtf --data simulation.fastq --kmer 15
