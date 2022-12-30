import pandas as pd
import os

os.chdir(os.path.dirname(__file__))


# Read HGNC symbol data
hgnc_symbol_df = pd.read_excel("HGNCsymbol_Accession_ID.xlsx")
# hgnc_symbol_df.drop(columns=("HGNC ID",))

# Read TRNA_Names
trna_names = pd.read_excel("TRNA_NAMES.xlsx", names=('A', 'B', 'C', 'D', 'E'))

hgnc_urs = pd.read_csv("human-tRNA.tsv", names=("URS", "pa", "HGNC ID", "pb", "pc"), sep='\t', index_col=False, usecols=[0, 2], skipinitialspace=True)

# Merge hgnc and trna names
trna_names_hgnc = trna_names.merge(hgnc_symbol_df, left_on='C', right_on="Approved symbol", how="inner")
trna_names_hgnc = trna_names_hgnc.merge(hgnc_urs, on="HGNC ID")

# Read mintbase_new
mintbase_new = "mintbase_new"

mintbase_new_names = ['Type_mintbase', 'MINTbase Unique ID (sequence derived)', 'Unique tRNA name', 'tRNA number', 
    'Amino acid and anticodon', 'Chromosome', 'Chromosome strand', 'Chromosome start position', 
    'Chromosome end position', 'Start position relative to start of mature tRNA', 
    'End position relative to start of mature tRNA', 'Fragment sequence', 'Fragment length', '']


mintbase_new_df = pd.read_csv(mintbase_new, header=None, sep='\t', comment='#', names=mintbase_new_names, 
                                            skip_blank_lines=True, skipinitialspace=True, usecols=mintbase_new_names[:-1]) # skip broken last column


# merge trfdb with trna_names_hgnc
mintbase_hgnc = mintbase_new_df.merge(trna_names_hgnc[["A", "Approved symbol", "Accession numbers", "HGNC ID", "URS"]], 
                                      left_on="Unique tRNA name", right_on='A')

mintbase_hgnc.to_csv("mintbase_new_HGNC_Accession.csv", sep='\t', index=False)

# Read trfdb
def read_trfdb_seg(filename):
    # trfdb =  os.path.join(folder_name, "trfdb_csv_result.csv")

    trfdb_df = pd.read_csv(filename, header=0, sep=',', skipinitialspace=True)

    # clear last space on sequence
    trfdb_df['tRF Sequence'] = trfdb_df['tRF Sequence'].str.strip()

    return trfdb_df


trfdb_segments = [read_trfdb_seg(os.path.join('tRF-1', 'trfdb_csv_result.csv')),
                  read_trfdb_seg(os.path.join('tRF-3', 'trfdb3_csv_result.csv')),
                  read_trfdb_seg(os.path.join('tRF-5', 'trfdb5_csv_result.csv'))]


trfdb_df = pd.concat(trfdb_segments)


# merge trfdb wit hgnc
trfdb_hgnc = trfdb_df.merge(trna_names_hgnc[["D", "Approved symbol", "Accession numbers", "HGNC ID", "URS"]],
                            left_on="tRNA Name", right_on='D')

trfdb_hgnc.to_csv("trfdb_HGNC_Accession.csv", sep='\t', index=False)