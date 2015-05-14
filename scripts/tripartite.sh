# Compute tripartite score of original and compressed cufflinks results (strict and loose
../../../compress-alignments/compareTripartite.py simulation.pro genes_fixed_sorted.gtf cufflinks/transcripts.gtf transcripts.gtf 1

echo ''
../../../compress-alignments/compareTripartite.py simulation.pro genes_fixed_sorted.gtf cufflinks/transcripts.gtf transcripts.gtf 0

