
'Run "Source script" in the upper right side from this pane for'
'1)functions_ensembl_query.py'
'2)classes.py'
'3)print_functions.py'
'4)HPA_download.py'


import urllib
import zipfile
import os.path
import csv
import requests
import re

##############Question flow#######################


a = 'Which gene(s) do you want to analyse?: '
a += '\n\t(Please, enter your ensembl gene ID(s) or hgnc symbol gene ID(s) separated by ",")'
a += '\n\t(Enter "q" if you want to terminate the program)'
a += '\ne.g. AK2 or ENSG00000004455, CXCL10'

b = 'Do you also want information about the related protein(s)?:'
b += '\n\t(Please, enter "yes" to get it or \n\t"q" if you want to terminate the program)'

c = '\nThere is some extensive information downloaded from Uniprot db.'
c += '\nEnter one or more of the following numbers (separated by ",") if you want to see it:' 
c +=  '\n\t1) Gene Ontology (molecular function)\n\t2) Gene Ontology (biological process)'
c +=  '\n\t3) Uniprot subcellular location\n\t4) Natural AAs variants\n\t5) Involvement in disease'
c +=  '\n\t6) For all of them\n\t7) Not needed, thank you'
c +=  '\n("q" if you want to terminate the program)'

message = []
message2 = []
message3 = []
gene_list = []
hgnc_list = []
geneInfo_dict = {}    #Create a dictionary where all the final data are saved
proteinInfo_dict = {}

while message != 'q':
  message = input(a).replace(" ", "") #"replace" to eliminate spaces in the input
  
  if message == 'q':
    print('Program is finished')
    break
  else:
    if "," in message:
      gene_list = message.split(",")
      for i in gene_list:
        print('\n* Retrieving information over ' + i.upper() +  ' gene\n')
        
        geneQuery = Gene(i)
        try:
          if geneQuery.complete_name:
            geneInfo_dict[geneQuery.gene_symbol] = geneQuery
        except AttributeError:
          continue
    else:
      print('\n* Retrieving information over ' + message.upper() +  ' gene\n')
      geneQuery = Gene(message)
      
      try:
        if geneQuery.complete_name:
            geneInfo_dict[geneQuery.gene_symbol] = geneQuery
      except AttributeError:
        break
        
    #print_gene_data(geneInfo_dict)
  
  answers = ['yes','q']
  message2 = input(b).lower()
  
  if message2 not in answers:
    print_gene_data(geneInfo_dict)
    print('\n\nPlease, enter a valid answer to get the protein information')
    print('Re-run the program if you still want it')
    print('Program is finished')
    break
  
  elif message2 == answers[0]:
    subcellular_data = HPA_import('subcellular_location.tsv')
    print('\n\tSubcellular location file from "Human Protein Atlas" has been loaded')      

    for key, value in geneInfo_dict.items():
      hgnc_list.append(key)
    for i in hgnc_list:
      print('\n* Retrieving information over ' + i.upper() +  ' related protein(s)\n')

      proteinQuery = Protein(i)
      proteinInfo_dict[proteinQuery.gene_symbol] = proteinQuery
    
  elif message2 == answers[1]:
    print_gene_data(geneInfo_dict)
    print("\n\n\tProgram is finished")
    break
  
  print_gene_data(geneInfo_dict)
  print_protein_data(proteinInfo_dict)

  answers_extra = ["1","2","3","4","5","6","7","q"]
  message3 = input(c)

  extended_strings = ['Gene Ontology (molecular function)', 'Gene Ontology (biological process)', 
  'Subcellular location [CC]',  'Natural variant', 'Involvement in disease']

  if "," in message3:
    selection_list = message3.split(",")
    for j in selection_list:      
      if j not in answers_extra:
        print('\n\nSelection "' + j + '" is not valid')
        print('Please, re-run the program and make a proper selection if you still want to see the information')
        print('Program is finished')
        break
      else:
        print('\n\nRetrieving "' + extended_strings[int(j)-1]  + '" from local database...\n\n')
        print_uniprot_extended(int(j)-1, proteinInfo_dict)

  elif message3 not in answers_extra:
    print('\n\nSelection "' + message3 + '" is not valid')
    print('Please, re-run the program and make a proper selection if you still want to see the information')
    print('Program is finished')
    break
  
  else:
    if message3.isnumeric():
      print_uniprot_extended(int(message3)-1, proteinInfo_dict)
    else:
      print('Program is finished')
      break
    
  break
