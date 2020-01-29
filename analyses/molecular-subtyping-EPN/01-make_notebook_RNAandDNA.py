#!/usr/bin/env python
# coding: utf-8





import pandas as pd
import numpy as np 

pbta_histologies = pd.read_csv("/Users/kogantit/Documents/OpenPBTA/OpenPBTA-analysis/data/pbta-histologies.tsv", sep="\t")

outnotebook = open("/Users/kogantit/Documents/OpenPBTA/OpenPBTA-analysis/analyses/molecular-subtyping-EPN/results/EPN_molecular_subtype.tsv", "w")

EP = pbta_histologies[pbta_histologies["disease_type_new"]=="Ependymoma"]
EP_rnaseq_samples = EP[EP["experimental_strategy"] == "RNA-Seq"][["Kids_First_Biospecimen_ID", "primary_site", "Kids_First_Participant_ID", "sample_id", "experimental_strategy"]]
EP_rnaseq_samples["disease_group"] = ["infratentorial" if "Posterior Fossa" in primary else "infratentorial" if "Optic" in primary else "supratentorial" if "Frontal Lobe" in primary else "supratentorial" if "Parietal Lobe" in primary else "infratentorial" if "Spinal Cord" in primary else "supratentorial" if "Occipital Lobe" in primary else "infratentorial" if "Tectum" in primary else "infratentorial" if "Spine" in primary else "supratentorial" if "Temporal Lobe" in primary else "infratentorial" if "Spinal" in primary else  "None" for primary in EP_rnaseq_samples["primary_site"]]


all_WGS = EP[EP["experimental_strategy"]=="WGS"]
WGSPT = all_WGS[all_WGS["Kids_First_Participant_ID"].isin(EP_rnasamplenames_PTIDs)]
WGS_dnaseqsamples = WGSPT[["Kids_First_Biospecimen_ID", "Kids_First_Participant_ID", "sample_id"]]

count =0 
for index1, row1 in EP_rnaseq_samples.iterrows():
    list_of_sampleids = []
    list_of_sampleids.append(row1["sample_id"])
    for index2, row2 in WGS_dnaseqsamples.iterrows():
        if (row1["sample_id"] == row2["sample_id"]) and (row1["Kids_First_Biospecimen_ID"] != row2["Kids_First_Biospecimen_ID"]):
            list_of_sampleids.append(row2["sample_id"])
            outnotebook.write(str(row1["Kids_First_Participant_ID"])+"\t"+str(row1["sample_id"])+"\t"+str(row2["Kids_First_Biospecimen_ID"])+"\t"+str(row1["Kids_First_Biospecimen_ID"])+"\t"+str(row1["disease_group"])+"\n")
    if len(list_of_sampleids) <2:
        outnotebook.write(str(row1["Kids_First_Participant_ID"])+"\t"+str(row1["sample_id"])+"\t"+"NA"+"\t"+str(row1["Kids_First_Biospecimen_ID"])+"\t"+str(row1["disease_group"])+"\n")
        
        
    
  





