# bioinf-proj
Methylation sites as a biomarker for cancer types - Bioinformatics project #4

##Interesting GDC Queries

***Adenomas and Adenocarcinomas***

cases.disease_type in ["Adenomas and Adenocarcinomas"]  
and cases.primary_site in ["Bronchus and lung"]  
and files.data_category in ["DNA Methylation"]  
and files.platform in ["Illumina Human Methylation 450"]  
and cases.samples.sample_type in ["Primary Tumor","Recurrent Tumor"] 

**files***: 437  

***cases***: 425  

***size***: 61.73 GB  


***Bronchus and lung***

cases.disease_type in ["Squamous Cell Neoplasms"]  
and cases.primary_site in ["Bronchus and lung"]  
and files.data_category in ["DNA Methylation"]  
and files.platform in ["Illumina Human Methylation 450"]  
and cases.samples.sample_type in ["Primary Tumor","Recurrent Tumor"] 

***files***: 370  

***cases***: 372  

***size***: 52.28 GB  


##Methylation Liftover Fields

* Composite Element: A unique ID for the array probe associated with a CpG site  
* Beta Value: Represents the ratio between the methylated array intensity and total array intensity,  
  falls between 0 (lower levels of methylation) and 1 (higher levels of methylation)  
* Chromosome: The chromosome in which the probe binding site is located  
* Start: The start of the CpG site on the chromosome  
* End: The end of the CpG site on the chromosome  
* Gene Symbol: The symbol for genes associated with the CpG site. 
  Genes that fall within 1,500 bp upstream of the transcription start site (TSS) to the end of the gene body are used.  
* Gene Type: A general classification for each gene (e.g. protein coding, miRNA, pseudogene)  
* Transcript ID: Ensembl transcript IDs for each transcript associated with the genes detailed above  
*Position to TSS: Feature Type Distance in base pairs from the CpG site to each associated transcript’s start site  
* CGI Coordinate: The start and end coordinates of the CpG island associated with the CpG site  
* Feature Type: The position of the CpG site in reference to the island: 
  Island, N_Shore or S_Shore (0-2 kb upstream or downstream from CGI), or N_Shelf or S_Shelf (2-4 kbp upstream or downstream from CGI)  

