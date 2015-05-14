# Compute precision and recall of original and compressed cufflinks results
echo 'Original:'
../../../compress-alignments/compareToTruth.py simulation.pro genes_fixed_sorted.gtf cufflinks/transcripts.gtf

echo ''
echo 'Compressed:'
../../../compress-alignments/compareToTruth.py simulation.pro genes_fixed_sorted.gtf transcripts.gtf
