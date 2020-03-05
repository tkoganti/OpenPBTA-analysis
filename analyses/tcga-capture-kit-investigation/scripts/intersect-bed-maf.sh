#!/bin/bash
##############################
# 
# This script intersects all the BED and then use that to intersect with 
# released PBTA and TCGA MAF and then counted all the mutation number within 
# that intersection region, and then mapped that counts to the project and 
# tumor type for each sample.
# 
##############################


## set data path variable 
DATA='../../data'
SCRATCH='../../scratch'


## get intersection between all the BED files
bedtools intersect -a $DATA/WGS.hg38.strelka2.unpadded.bed -b $DATA/WGS.hg38.mutect2.vardict.unpadded.bed \
| bedtools intersect -a - -b $DATA/WGS.hg38.lancet.unpadded.bed \
| bedtools intersect -a - -b results/whole_exome_agilent_1.1_refseq_plus_3_boosters.targetIntervals.Gh38.bed \
| bedtools intersect -a - -b results/whole_exome_agilent_designed_120.targetIntervals.Gh38.bed \
| bedtools intersect -a - -b results/whole_exome_agilent_plus_tcga_6k.targetIntervals.Gh38.bed \
| bedtools intersect -a - -b results/tcga_6k_genes.targetIntervals.Gh38.bed \
> $SCRATCH/intersect-all-tcga_pbta.bed


## get all the PBTA and TCGA maf into BED-like format and intersect with 
## the region generated by the above step
for caller in 'lancet' 'mutect2' 'strelka2'
do
    zcat $DATA/pbta-snv-$caller.vep.maf.gz \
    | sed 1,2d | cut -f5-7,16 \
    | bedtools intersect -a - -b $SCRATCH/intersect-all-tcga_pbta.bed \
    | cut -f4 | sort | uniq -c \
    | awk -v c=$caller 'BEGIN{OFS="\t"}{print $2,$1,"PBTA",c}';
    zcat $DATA/pbta-tcga-snv-$caller.vep.maf.gz \
    | sed 1,2d | cut -f5-7,16 \
    | bedtools intersect -a - -b $SCRATCH/intersect-all-tcga_pbta.bed \
    | cut -f4 | sort | uniq -c \
    | awk -v c=$caller 'BEGIN{OFS="\t"}{print $2,$1,"TCGA",c}';
done > $SCRATCH/somatic-count.tsv


## matching histology for the mutation counts file generated by the step above
touch $SCRATCH/tumor_type.tsv
sed 1d $DATA/pbta-histologies.tsv | cut -f1,17 > $SCRATCH/tumor_type.tsv && \
sed 1d $DATA/pbta-tcga-manifest.tsv | cut -f2,5 >> $SCRATCH/tumor_type.tsv
cat $SCRATCH/somatic-count.tsv | cut -f1 \
| while read i
do
    grep $i $SCRATCH/tumor_type.tsv | cut -f2
done | paste $SCRATCH/somatic-count.tsv - > $SCRATCH/somatic-count_with-histologies.tsv