######################################################################

###Auxiliary function for ensembl phenotypes

def remove_duplicates(dictionary_list):
  '''Check if "description" string is present in the dictionary list from ensembl phenotype query'''
    
  unique_keys = []  # empty dictionary for tracking unique keys
  result = []  # new list for storing a dictionary without duplicate keys
    
  for d in dictionary_list:
    if d['description'] in unique_keys:
      continue  # skip this dictionary as it has a duplicated key
    else:  # executed only if the for loop completes without hitting a break
      result.append(d)  # add the dictionary to the result list
      unique_keys.append(d['description'])  # update unique description
      
  return result

####Auxiliary function for HPA
def check_string_in_dict(string, dictionary):
  '''Check if a certain input string is present in any of the values from a dictionary key-value pair'''
  
  for value in dictionary.values():
    if value == string:
      return True
  return False

######################################################################
def ensembl_query(*gene_name):
  '''Query ensembl API information about a gene with ensembl ID or hgnc symbol'''

  import requests
 
  server = "https://rest.ensembl.org"
  headers_gene={ "Content-Type" : "application/json", "Accept" : "application/json"}
  headers_others={ "Content-Type" : "application/json"}
  
  geneInfo_dict = {}
  gene_basics = {}

  for gene in gene_name:
    
    if gene.startswith("ENSG"):
      ext = "/lookup/id"
      ext_xref = "/xrefs/id/" + gene + "?"
      data_obj ='{"ids" : ["' + gene + '"]}'
    else:
      ext = "/lookup/symbol/homo_sapiens"
      ext_xref = "/xrefs/name/human/" + gene + "?"
      data_obj ='{"symbols" : ["' + gene + '"]}'
    
    ext_pheno = "/phenotype/gene/homo_sapiens/" + gene + "?trait=1" #Both ensembl and symbol accepted in this ext
  
    #Query for gene IDs (hgnc symbol, gene type, complete name and ensembl ID)
    r = requests.post(server+ext, headers = headers_gene, data = data_obj)
    if not r.ok:
      break
    
    #Query for gene xrefs (hgnc synonyms, entrez IDs and uniprot IDs)
    r_xref = requests.get(server+ext_xref, headers = headers_others)
    if not r_xref.ok:
      break

    #Query for gene phenotypes (associated diseases)
    r_pheno = requests.get(server+ext_pheno, headers = headers_others)  
    if not r_pheno.ok:
      break

    decoded = r.json()
    decoded_xref = r_xref.json()
    decoded_pheno = r_pheno.json()
    
    for i in decoded:
      gene_basics ["hgnc_name"] = decoded[i]['display_name']
      gene_basics ["ensembl_id"] = decoded[i]['id']
      gene_basics ["gene_type"] = decoded[i]['biotype']
      gene_basics ["complete_name"] = decoded[i]['description']
    
    hgnc_synonyms = []
    entrez_id = []
    uniprot_id = []
  
    for a in decoded_xref:
      
      if a['dbname']=="HGNC":
        for s in a['synonyms']:
          hgnc_synonyms.append(s)

      elif a['dbname']=="EntrezGene":
        entrez_id = a['primary_id']
      
      else:
        continue

    subset_uniprot = [d for d in decoded_xref if d['dbname']=="Uniprot_gn" ]
    uniprot_id = [f['primary_id'] for f in subset_uniprot]

    if hgnc_synonyms:
      gene_basics ["hgnc_synonyms"] = hgnc_synonyms
    else:
      gene_basics ["hgnc_synonyms"] ='None'

    if entrez_id:
      gene_basics ["entrez_id"] = entrez_id
    else:
      gene_basics ["entrez_id"] = 'None'
    
    gene_basics ["uniprot_id"] = uniprot_id
    

    ontology_complete_list = []
    ontology_list = []
    
    ontology_complete_list = remove_duplicates(decoded_pheno) #Remove description duplicates from the list 
    ontology_complete_list = sorted(ontology_complete_list, key=lambda x: x['description'])  

    
    for i in ontology_complete_list: #select only description and ontology accessions
      partial_dict = {key: value for key, value in i.items() if key in ['description', 'ontology_accessions']}
      ontology_list.append(partial_dict)

    if ontology_list:
      gene_basics ["phenotypes"] = ontology_list
      geneInfo_dict[gene] = gene_basics

    else:
      gene_basics ["phenotypes"] = 'None'
      geneInfo_dict[gene] = gene_basics
      continue

  return(geneInfo_dict)
  
######################################################################

######Protein related functions

def protein_query(*identifier):
  '''Rerieve uniprot IDs from "gene_dict" created after "ensembl_xref" function'''
  
  proteinInfo_dict = {}
  protein_basics = {}
  protein_hpa_location = {}

  for id in identifier:

    protein_HPA_list = []  
    for i in subcellular_data:  #Check 'subcellular location' in downloaded HPA data base
      protein_HPA_list.append(i['Gene name'])
      
    if any(id == p for p in protein_HPA_list) == True:
      for i in subcellular_data:
        if check_string_in_dict(id, i):
          protein_hpa_location ['main_location'] = i['Main location']
          protein_hpa_location ['additional_location'] = i['Additional location']
          protein_hpa_location ['extracellular_location'] = i['Extracellular location']
          protein_hpa_location ['cell_cycle'] = i['Cell cycle dependency']
          protein_hpa_location ['reliability'] = i['Reliability']
          protein_hpa_location ['go_id'] = i['GO id']

          protein_basics ["hpa_location"] = protein_hpa_location
    else:
      protein_basics ["hpa_location"] = 'Not found'
    
    unipQuery = uniprot_query(id)
    protein_basics ['uniprot_query'] = unipQuery
    
    try:
      protein_basics ["uniprot_id"] = unipQuery["Entry"]
    except KeyError:
      print('\t\tThere is no Uniprot entry in the database for ' + id + ' gene')
      break    
    
  proteinInfo_dict[id] = protein_basics

  return(proteinInfo_dict)

######UNIPROT

def uniprot_query(*prot_identifier):
  '''Query to uniprot API about a gene with ensembl ID or hgnc symbol'''
  
  import requests

  uniprot_dict = {}
  
  for id in prot_identifier: 
    try:
      url = 'https://rest.uniprot.org/uniprotkb/search?&query=gene_exact:' + id + '+AND+organism_id:9606+AND+database:pdb&format=tsv&fields=gene_primary,protein_name,accession,organism_name,length,mass,sequence,cc_tissue_specificity,go_p,go_f,cc_function,cc_subcellular_location,ft_variant,cc_disease'
      if not requests.get(url).ok:
        break
      query = requests.get(url).text.split("\n")#Query to uniprot based on the provided url 
    
    except TypeError:
      continue
    
    query_headers =query[0].split("\t") #Get col names of the tsv from uniprot
    query_values =query[1].split("\t") #Get the information under the col names

    res = dict(zip(query_headers, query_values))#Make a dictionary out of headers and values
    uniprot_dict= res #Add to dictionary
    
  return(uniprot_dict)
