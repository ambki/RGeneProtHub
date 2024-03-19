import urllib
import zipfile
import requests
import os
import csv


def HPA_import(file):

  url = 'https://www.proteinatlas.org/download/subcellular_location.tsv.zip'
  
  if os.name == 'posix':
    extract_dir = './downloads'
    check_file = os.path.isfile(extract_dir + '/' + file)
  elif os.name == 'nt':
    extract_dir = '.\downloads'
    check_file = os.path.isfile(extract_dir + '\\' + file)
  
  if check_file == False:
    input('\nHuman Protein Atlas subcellular location file does not exist and it is going to be downloaded\n\nPress enter to continue...')

    zip_path, _ = urllib.request.urlretrieve(url)
    with zipfile.ZipFile(zip_path, "r") as f:
      f.extractall(extract_dir)
    print("File downloaded successfully")

    subcellular_data = []

    with open(extract_dir + '/' + file, 'r') as file:
      csv_reader = csv.DictReader(file, delimiter='\t')
      # Iterate over each row
      for row in csv_reader:
            # Check and fill empty values with "N/A"
          for key, value in row.items():
            if not value:
              row[key] = 'N/A'  
          subcellular_data.append(row)
    
    return(subcellular_data)    
  
  else:
    subcellular_data = []

    with open(extract_dir + '/' + file, 'r') as file:
      csv_reader = csv.DictReader(file, delimiter='\t')
      # Iterate over each row
      for row in csv_reader:
            # Check and fill empty values with "N/A"
          for key, value in row.items():
            if not value:
              row[key] = 'N/A'  
          subcellular_data.append(row)
          
    return(subcellular_data)
    # The "subcellular_data"" variable then holds a list of dictionaries, where each dictionary 
    #represents a row from the TSV file. The keys of the dictionaries are the column headers, 
    #and the values are the corresponding data.
    
