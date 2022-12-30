import pandas as pd
import sqlalchemy

DB_USER = "diamantop"
DB_PASSWORD = "12345678"
DB_HOSTNAME = "pez.insybio.com"
DB_PORT = "3306"
DB_NAME = "diamantop_ncrnas"
DB_TABLE = "genes"

DB_COLS = ['gene_stable_id','protein_stable_id','transcript_stable_id',
            'gene_description', 'gene_end', 'gene_start', 'strand',
            'transcript_start','gencode_basic_annotation', 'refseq_match_transcript', 
            'gene_name', 'GO_term_accession', 'ensemble_protein_family_id']





print('Reading file...')

# read data into pandas dataframe
df = pd.read_csv("martquery_1031102737_477.txt", sep=',', header=0)

df.dropna('columns', 'all', inplace=True)
df.drop(['Gene stable ID version', 'Source of gene name', 'Source (gene)', 'Ensembl Family Description'], 'columns', inplace=True)

# column rename
df.columns = DB_COLS

print('Removing dupliacates')

df.drop_duplicates(subset='gene_stable_id', keep='first', inplace=True, ignore_index=True)

print(df.columns)

hgnc_id = df['gene_description'].str.extract(r'HGNC:(\d*)')
print(hgnc_id.head(5))
df['hgnc_id'] = hgnc_id

df.to_csv("genes_to_db.csv", sep='\t', na_rep='NULL')

# input()
# print('Total element after duplicate-removal on primary key:', len(df))

# exit()
# # connet to mySQL db
# print('Connecting to database...')

# engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}')

# # df_one = df[:1]

# # print(df_one)
# print('Writing to database...')

# df.to_sql(DB_TABLE, engine, if_exists='append', index=False, chunksize=50)

