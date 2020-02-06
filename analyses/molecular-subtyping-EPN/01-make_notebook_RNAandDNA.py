#!/usr/bin/env python
#Author - Teja Koganti (D3B)


import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--histologies', required = True,
                    help = 'path to the histology file')
parser.add_argument('-o', '--outnotebook', required = True,
                    help = "output notebook")
args = parser.parse_args()

pbta_histologies = pd.read_csv(args.histologies, sep="\t")
outnotebook = open(args.outnotebook, "w")

# Based on primary site, supra/infra category  assigned to each sample
# These two primary sites could not be categorized  and will be assigned "None" under disease group
#		"Other locations NOS" and "Ventricles"
def group_disease(primay_site):
	if "Posterior Fossa" in primay_site:
		return "infratentorial"
	elif "Optic" in primay_site:
		return "infratentorial"
	elif "Spinal" in primay_site:
		return "infratentorial"
	elif "Tectum" in primay_site:
                return "infratentorial"
	elif "Spine" in primay_site:
                return "infratentorial"
	elif "Frontal Lobe" in primay_site:
		return "supratentorial"
	elif "Parietal Lobe" in primay_site:
                return "supratentorial"
	elif "Occipital Lobe" in primay_site:
		return "supratentorial"
	elif "Temporal Lobe" in primay_site:
                return "supratentorial"
	else:
		return "None"

# Filtering for ependymoma samples 
EP = pbta_histologies[pbta_histologies["disease_type_new"]=="Ependymoma"]
EP_rnaseq_samples = EP[EP["experimental_strategy"] == "RNA-Seq"][["Kids_First_Biospecimen_ID", "primary_site", 
	"Kids_First_Participant_ID", "sample_id", "experimental_strategy"]]
EP_rnaseq_samples["disease_group"] = [group_disease(primary) for primary in EP_rnaseq_samples["primary_site"]]
# List with only RNA samples
EP_rnasamplenames_PTIDs = list(EP_rnaseq_samples["Kids_First_Participant_ID"]) 

# Filtering for DNA samples 
all_WGS = EP[EP["experimental_strategy"]=="WGS"]
WGSPT = all_WGS[all_WGS["Kids_First_Participant_ID"].isin(EP_rnasamplenames_PTIDs)]
WGS_dnaseqsamples = WGSPT[["Kids_First_Biospecimen_ID", "Kids_First_Participant_ID", "sample_id"]]

# Renaming the column name so they don;t conflict in merge step 
EP_rnaseq_samples = EP_rnaseq_samples.rename(columns={"Kids_First_Biospecimen_ID":"Kids_First_Biospecimen_ID_RNA"})
WGS_dnaseqsamples = WGS_dnaseqsamples.rename(columns={"Kids_First_Biospecimen_ID":"Kids_First_Biospecimen_ID_DNA"})

# sample_id is common between both  datafarmes and also unique between RNA and DNA. 
# Some DNA BSID's are missing for the corresponding RNA samples 
EP_rnaseq_WGS = EP_rnaseq_samples.merge(WGS_dnaseqsamples, on = "sample_id", how = "left")
EP_rnaseq_WGS = EP_rnaseq_WGS.rename(columns={"Kids_First_Participant_ID_x":"Kids_First_Participant_ID"})
EP_rnaseq_WGS.fillna('NA', inplace=True)

EP_rnaseq_WGS[["Kids_First_Participant_ID", "sample_id", "Kids_First_Biospecimen_ID_DNA", "Kids_First_Biospecimen_ID_RNA", "disease_group"]].to_csv(outnotebook, sep="\t", index=False)
outnotebook.close()
    
