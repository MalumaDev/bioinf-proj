
import requests
import json
import re
import tarfile
import os
import shutil


'''
    ---------- 
  getData(disease_type=[], path=".", file_n, unzip=True)
      disease_type: list of disease as ["Adenomas and Adenocarcinomas","Squamous Cell Neoplasms"]
      path: location where to download and extract genomic files
      file_n: number of files to be downloaded (to know the size see GDM website)
      unzip: False for the tar-gzipped dataset; True for data unzip and extraction
      
    ----------
'''

def main():
    
   getData(path="/home/emil/prova"); #["Squamous Cell Neoplasms"]

   

def getData(disease_type=["Adenomas and Adenocarcinomas","Squamous Cell Neoplasms"], path=".", file_n=2, unzip=True):
    #Query example:
    #cases.disease_type in ["Adenomas and Adenocarcinomas","Squamous Cell Neoplasms"] 
    #and cases.primary_site in ["Bronchus and lung"] 
    #and files.data_category in ["DNA Methylation"] 
    #and files.platform in ["Illumina Human Methylation 450"] 
    #and cases.samples.sample_type in ["Primary Tumor","Recurrent Tumor"]
    
    files_endpt = "https://api.gdc.cancer.gov/files"
    
    filters = {
        "op": "and",
        "content":[
            {
            "op": "in",
            "content":{
                "field": "cases.disease_type",
                "value": disease_type 
                }
            },
            {
            "op": "in",
            "content":{
                "field": "cases.primary_site",
                "value": ["Bronchus and lung"] 
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.data_category",
                "value": ["DNA Methylation"] 
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.platform",
                "value": ["Illumina Human Methylation 450"]  
                }
            },
            {
            "op": "in",
            "content":{
                "field": "cases.samples.sample_type",
                "value": ["Primary Tumor","Recurrent Tumor"]  
                }
            }           
        ]
    }
    
    # A POST is used, so the filter parameters can be passed directly as a Dict object.
    params = {
        "filters": filters,
        "fields": "file_id",
        "format": "JSON",
        "size": file_n
        }
    
    # The parameters are passed to 'json' rather than 'params' in this case
    response = requests.post(files_endpt,
                             headers = {"Content-Type": "application/json"}, 
                             json = params)
    #print(response.content.decode("utf-8"))
    
    file_uuid_list = []

    # This step populates the download list with the file_ids from the previous query
    # JSON format is { "data": { "hits": ["file_id":"...", "id":"..." ] } }
    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])
        
    print("list of files to be downloaded:\n",file_uuid_list)
    
    data_endpt = "https://api.gdc.cancer.gov/data"
    
    params = {"ids": file_uuid_list}
    
    print("download in progress...")
    #query data corresponding to file ids
    response = requests.post(data_endpt, 
                             data = json.dumps(params), 
                             headers = {"Content-Type": "application/json"}
                             )

    
    response_head_cd = response.headers["Content-Disposition"]
    #print("resp headers", response.headers)
    file_name = path+"/"+ re.findall("filename=(.+)", response_head_cd)[0]
    #print("filename ",file_name)
    with open(file_name, "wb") as output_file:
        output_file.write(response.content)
    print("data downloaded")
    
    if unzip: 
        print("extracting data...")
        unzipFile(file_name, path)
        extractFilesFromDirs(file_uuid_list, path)
        print("data extracted")
        
    
def unzipFile(fname,path="."):
    
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=path)
        tar.close()
    elif (fname.endswith("tar")):
        tar = tarfile.open(fname, "r:")
        tar.extractall(path=path)
        tar.close()
    
def extractFilesFromDirs(dir_list, path="."):
    #extract downloaded and unzipped files from directories 
    #in path, whose name is in dir_list
    for dir in dir_list:
        filepath= path+"/"+dir
        #print(filepath)
        for root, dirs, files in os.walk(filepath, topdown=False):
            for file in files:
                try:
                    #print(file)
                    shutil.move(filepath+"/"+file, path+"/"+file)
                except OSError:
                    pass
                #delete directories
                shutil.rmtree(filepath)
                      

if __name__ == "__main__":
    main()
    
'''
A typical search and retrieval API request specifies the following parameters:
    - a filters parameter, that specifies the search terms for the query
    - several parameters that specify the API response, such as:
        format — specifies response format (JSON, TSV, XML)
        fields — specifies the which data elements should be returned in the response, if available
        size — specifies the the maximum number of results to include in the response

The choice of endpoint determines what is listed in the search results. 
    The files endpoint will generate a list of files
    The cases endpoint will generate a list of cases. 
The cases endpoint can be queried for file fields 
    (e.g. to look for cases that have certain types of experimental data), 
The files endpoint can be queried for clinical metadata associated with a case 
    (e.g. to look for files from cases diagnosed with a specific cancer type).

The field operand specifies a field that corresponds to a property defined in the GDC Data Dictionary. 
    A list of supported fields is provided in Appendix A;
    can also be accessed programmatically at the _mapping endpoint.
The value operand specifies the search terms. 

'''