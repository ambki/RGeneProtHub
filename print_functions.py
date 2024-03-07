    
def print_gene_data(gene_dictionary):
  '''Print all info contained in Gene class'''
  
  print("\n##########################################################")
  print("\t\tGene Information".upper())
  print("##########################################################")
  
  for i in gene_dictionary:  
    try:    
      print("\n***************************\n")
      print("Ensembl ID: " + gene_dictionary[i].ensembl_id)
      print("HGNC symbol: " + gene_dictionary[i].gene_symbol.upper())
      print("Gene type: " + gene_dictionary[i].gene_type)
      print("Complete name: " + gene_dictionary[i].complete_name)
    except AttributeError:
      print('\t\t*** Gene information for ' + i.upper() + ' is EMPTY ***')
      continue

    print("\nHGNC synonyms: ") 
    if gene_dictionary[i].hgnc_synonyms != 'None':
      for s in gene_dictionary[i].hgnc_synonyms:
        print("\t-" + s)
    else:
      print('\n\t- There are no HGNC synonyms in ensembl database for ' + i + ' gene.')
  
    if gene_dictionary[i].entrez_id != 'None':
      print('\nEntrez ID: ' + gene_dictionary[i].entrez_id)
    else:
      print('\nEntrez ID: \n\t- There are no entrez IDs in ensembl database for ' + i+ ' gene.\n')
    if gene_dictionary[i].disease != 'None':
      print('\nPathologies caused by variations of ' + i.upper() + 
      ': \n(these variations could be of any nature: expression levels, mutations, ...)')
  
      for dis in gene_dictionary[i].disease:
        print("\n\t- " + dis['description'].title())
    
        if 'ontology_accessions' in dis.keys():
          for acc in dis['ontology_accessions']:
            print("\t\t" + acc)
        else:
          print('\t\t***There are no IDs for this disease in ensembl***')
          continue
    else:
      print('\nThere are no entries in ensembl database about diseases associated with ' + i + ' gene.')
      continue


######PROTEIN
def retrieve_uniprotID(string_list):
    '''Function to get a string which starts with a certain letter from a list of strings'''
    
    import re
    
    for string in string_list:        #letters based on accession IDs in Uniprot db
        if string.startswith('P'):
            return string
        elif string.startswith('Q'):
            return string
        elif string.startswith('O'):
            return string
    return None
  
def print_protein_data(protein_dictionary):
  '''Print all info contained in Protein class coming from ensembl and HPA'''
  
  print("\n##########################################################")
  print("\t\tProtein Information".upper())
  print("##########################################################")

  for i in protein_dictionary:  
    try:  
      print("\n***************************\n")
      print("Uniprot ID(s) for " + i.upper() +  ' (' + 
      retrieve_uniprotID(protein_dictionary[i].uniprot_id) + ')'+ " protein: (Source: ENSEMBL)")
      for u in protein_dictionary[i].uniprot_id:
        print("\t- " + u)
    except AttributeError:
      print('\t\t*** Protein information for ' + i.upper() + ' is EMPTY ***')
      continue
    
    if protein_dictionary[i].location != 'Not found':
      print('\nSubcellular location of ' + i.upper() + ' protein: (Source: HPA)' +
      '\n\t- Main: ' + protein_dictionary[i].location['main_location'] +
      '\n\t- Additional: ' + protein_dictionary[i].location['additional_location'] +
      '\n\t- Extracellular location: ' + protein_dictionary[i].location['extracellular_location'] +
      '\n\t- Cell cycle dependency: ' + protein_dictionary[i].location['cell_cycle'] + 
      '\n\t- Reliability: ' + protein_dictionary[i].location['reliability'] + 
      '\n\t- GO Id: ' + protein_dictionary[i].location['go_id'])
    else:
      print('\nSubcellular location of ' + i.upper() +' related protein(s)' +
      ' (ID: ' + retrieve_uniprotID(protein_dictionary[i].uniprot_id) + ')' +
      ': (Source: HPA)')
      print('\t- There is no subcellular location record in HPA database about ' +  i.upper() + ' related protein.')
      print('\t- This could be due to: \n\t\t1) a real absence of information in HPA') 
      print('\t\t2) the protein is always or most of the times secreted')
      print('\n\t(Checking in Uniprot db...)')
      
      if protein_dictionary[i].uniprot_info:
        for key, value in protein_dictionary[i].uniprot_info.items():
          if key in 'Subcellular location [CC]':
            print('\nSubcellular location of ' + i.upper() +' related protein(s)' +
            ' (ID: ' + retrieve_uniprotID(protein_dictionary[i].uniprot_id) + ')' +
            ': (Source: UNIPROT)')
            for j in value.split('.; '):
              print('\t- ' + re.sub('SUBCELLULAR LOCATION: ','', j))
          elif not key:
            continue
      else:
        print('\n(UNIPROT information for ' + i + ' is EMPTY) ')
        continue
    
    if protein_dictionary[i].uniprot_info:
      print('\n\t\t|---------(Source: UNIPROT)---------|')
      
      for key, value in protein_dictionary[i].uniprot_info.items():
        go_strings = ['Gene Ontology (molecular function)', 'Gene Ontology (biological process)' ]
        short_strings = ['Entry', 'Organism']
        quant_strings = ['Length', 'Mass']
      
        if key in short_strings:
          print('\n' + key + ': ' + value)
        
        elif key in 'Gene Names (primary)':
          print('\nHGNC symbol: ' + value)
        
        elif key in 'Protein names':
          val = re.split("\((.*?)\) ", value)
          val = list(filter(str.strip, val))
          print('\nProtein name(s): ' + val[0])
        
        elif key in 'Length':
          print('\n' + key + ': ' + value + ' AAs')
        
        elif key in 'Mass':
          print('\n' +key + ': ' + value + ' Da')
        
        elif key in 'Sequence':
          print('\n' + key + ': \n\n' + value)
        
        elif key in 'Tissue specificity':
          if not value:
            print('\n' + key + ': N/A')
          else:
            print('\n' + key + ':')
            print('\n\t- ' + re.sub('TISSUE SPECIFICITY: ','', value))
        
        elif key in 'Function [CC]':
          print('\n' + 'Function description:')
          print('\n\t- ' + re.sub('FUNCTION: ','', value) + '\n')
    
    else:
      print('\n(UNIPROT information for ' + i + ' is EMPTY) ')
      break

      
      
def print_uniprot_extended(selection, protein_dictionary):
  '''Print user selected info contained in Protein class coming from UNIPROT'''
    
  import re
  
  extended_strings = ['Gene Ontology (molecular function)', 'Gene Ontology (biological process)', 
  'Subcellular location [CC]',  'Natural variant', 'Involvement in disease']
  
  for i in protein_dictionary:
    print('\n**********Loading selected Information of ' + i  + ' related protein from UNIPROT database**********')
    
    if protein_dictionary[i].uniprot_info:
      for key, value in  protein_dictionary[i].uniprot_info.items():
        if selection == 0 and key in extended_strings[selection]:
          #'Gene Ontology (molecular function)':
          if not value:
            print('\n' + key + ': N/A')
          else:
            print('\n' + key + ':')
            for i in value.split("; "):
              print('\t- ' + i)
      
        if selection == 1 and key in extended_strings[selection]:  
          #'Gene Ontology (biological process)':
          if not value:
            print('\n' + key + ': N/A')
          else:
            print('\n' + key + ':')
            for i in value.split("; "):
              print('\t- ' + i)

        if selection == 2 and key in extended_strings[selection]:  
          #'Subcellular location [CC]':
          if not value:
            print('\n' + 'Subcellular location: N/A')
          else:
            print('\n' + 'Subcellular location:')
            for i in value.split('.; '):
              print('\n\t- ' + re.sub('SUBCELLULAR LOCATION: ','', i))
    
        if selection == 3 and key in extended_strings[selection]:
          #'Natural variant':
          if not value:
            print('\n' + key + '(s): N/A')
          else:
            value = re.sub('/note', 'Description', value)
            value = re.sub('/', '', value)
            print('\n' + key + '(s):')
            for i in value.split('; VARIANT '):
              print('\n\t- Position ' + re.sub('VARIANT','', i))
    
        if selection == 4 and key in extended_strings[selection]:  
          #'Involvement in disease':
          if not value:
            print('\n' + key + ': N/A')
          else:
            print('\n' + key + ':')
            for i in value.split('; DISEASE:'):
              print('\n\t- ' + re.sub('DISEASE: ','', i))
        
        if selection == 5:  
          #All
#          for key in extended_strings:
          if key in list( extended_strings[i] for i in [0,1] ):
            if not value:
              print('\n' + key + ': N/A')
            else:
              print('\n' + key + ':')
              for i in value.split("; "):
                print('\t- ' + i)
          elif key in 'Subcellular location [CC]':
            if not value:
              print('\n' + key + ': N/A')
            else:
              print('\n' + 'Subcellular location:')
              for i in value.split('.; '):
                print('\n\t- ' + re.sub('SUBCELLULAR LOCATION: ','', i))
          elif key in 'Natural variant':
            if not value:
              print('\n' + key + ': N/A')
            else:
              value = re.sub('/note', 'Description', value)
              value = re.sub('/', '', value)
              print('\n' + key + '(s):')
              for i in value.split('; VARIANT '):
                print('\n\t- Position ' + re.sub('VARIANT','', i))
          elif key in 'Involvement in disease':
            if not value:
              print('\n' + key + ': N/A')
            else:
              print('\n' + key + ':')
              for i in value.split('; DISEASE:'):
                print('\n\t- ' + re.sub('DISEASE: ','', i))

        if selection == 6:
          print('No more information printed')
          break
