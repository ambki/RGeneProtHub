class Gene():
  '''A class to model a Gene'''
  def __init__(self, gene_symbol):
    '''Initialize gene_symbol to reach out the rest of gene attributes
    in ensembl resting server'''
    
#ensembl db geneInfo_dict for specific information about the gene    
    gQuery = ensembl_query(gene_symbol)
    try:
        self.gene_symbol = gQuery[gene_symbol]['hgnc_name']
        self.ensembl_id = gQuery[gene_symbol]['ensembl_id']
        self.gene_type =  gQuery[gene_symbol]['gene_type']
        self.complete_name = gQuery[gene_symbol]['complete_name']
        self.hgnc_synonyms = gQuery[gene_symbol]['hgnc_synonyms']
        self.entrez_id = gQuery[gene_symbol]['entrez_id']
        self.uniprot_id = gQuery[gene_symbol]['uniprot_id']
        self.disease = gQuery[gene_symbol]['phenotypes'] 
    except KeyError:
      self.gene_symbol = gene_symbol.upper()
      print("\nSorry, but " + gene_symbol.upper() + " was not found in ENSEMBL database. Please, check your syntax or try with another gene.")
      print("NOTE: It could also be that the ENSEMBL server is saturated. If not a syntax problem, please, try again in a couple of minutes")
    

class Protein():
  '''A class to model a Protein'''
  def __init__(self, gene_symbol):
    '''Initialize gene_symbol to reach out the associated protein attributes in 
    ensembl resting server'''
    
    self.gene_symbol = gene_symbol.upper()
    pQuery = protein_query(gene_symbol)
    
    self.location = pQuery[gene_symbol]['hpa_location']
    try:
      self.uniprot_id = pQuery[gene_symbol]['uniprot_id']
      self.uniprot_info = pQuery[gene_symbol]['uniprot_query']
    except KeyError:
      print("\nSorry, but " + gene_symbol.upper() + " was not found in UNIPROT database. Please, check your syntax or try with another protein.")
      print("NOTE: It could also be that the UNIPROT server is saturated. If not a syntax problem, please, try again in a couple of minutes")
     
