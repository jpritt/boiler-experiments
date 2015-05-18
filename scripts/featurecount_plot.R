# Run me from the featurecounts_* results directory

ucomp_gene <- read.table('uncompressed/counts_gene.tsv', header=T)
comp_gene <- read.table('compressed/counts_gene.tsv', header=T)

ucomp_exon <- read.table('uncompressed/counts_exon.tsv', header=T)
comp_exon <- read.table('compressed/counts_exon.tsv', header=T)

pdf(file="gene.pdf")
plot(log10(ucomp_gene[,7]), log10(comp_gene[,7]),
     xlim=c(0, 6), ylim=c(0, 6),
     xlab="Log10 uncompressed count", ylab="Log10 compressed count",
     col=rgb(0, 0, 0, 0.1),
     main="Gene counts before and after compression")
abline(0, 1, col="red")
dev.off()

pdf(file="exon.pdf")
plot(log10(ucomp_exon[,7]), log10(comp_exon[,7]),
     xlim=c(0, 6), ylim=c(0, 6),
     xlab="Log10 uncompressed count", ylab="Log10 compressed count",
     col=rgb(0, 0, 0, 0.1),
     main="Exon counts before and after compression")
abline(0, 1, col="red")
dev.off()
