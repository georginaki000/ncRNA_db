import pandas as pd
import sqlalchemy
import time
from tqdm import tqdm
import os

DB_USER = "diamantop"
DB_PASSWORD = "12345678"
DB_HOSTNAME = "pez.insybio.com"
DB_PORT = "3306"
DB_NAME = "diamantop_TEST15"



def send_to_db_with_delay(conn, df, table_name,  col_name_transform=None, chunksize=100, t_delay=0.01, primary_key=None):

    if col_name_transform is not None:
        # keep specific columns
        df = df[[*col_name_transform]]
        # rename columns
        if type(col_name_transform) is dict:
            df.rename(columns=col_name_transform, inplace=True)
            
    if primary_key and primary_key in df.columns:
        df.drop_duplicates(subset=primary_key, keep='first', inplace=True, ignore_index=True)
    
    num_chunks = len(df) // chunksize + 1
    print(f'Sending {len(df)} entries to {table_name}')
    for i in tqdm(range(num_chunks)):
        chunk = df[i*chunksize: min(len(df), (i+1)*chunksize)]
        chunk.to_sql(name=table_name, con=conn, if_exists='append', index=False, method='multi')
        time.sleep(t_delay)

# PREPROCCESS

print("Running: chunk_martquery")
import chunk_martquery

print("Running: hairpin_fa_read")
import hairpin_fa_read

print("Running: HGNC_symbols")
import HGNC_symbols

print("Running: mintbase_new_tRF_db")
import mintbase_new_tRF_db

print("Running: mirna_mature_mature")
import mirna_mature_mature

print("Running: mirna_txt_mirna_dat")
import mirna_txt_mirna_dat

print("Running: parse_miRNA_dat")
import parse_miRNA_dat

print("Running: read_human_mirna_mature")
import read_human_mirna_mature

print("Running: unique_sequences")
import unique_sequences

print("Running: write_to_db_genes")
import write_to_db_genes

print("Running: write_to_db_proteins")
import write_to_db_proteins

print("Running: genes_proteins")
import genes_proteins

print("Running: mirnas_genes")
import mirnas_genes

print("Running: Function.function_main")
import Function.function_main

print("Running: sequence_predictions.clear_data")
import sequence_predictions.clear_data

print("Running: sequences.seperate_RNAs")
import sequences.seperate_RNAs


os.chdir(os.path.dirname(__file__))

# create database
engine =  sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}')
with engine.begin() as conn:
    with open("../DATABASE_SCHEMA.sql", 'r') as f:
        conn.execute(f"CREATE DATABASE {DB_NAME};")
        conn.execute(f"USE DATABASE {DB_NAME};")

        schema_file = sqlalchemy.text(f.read())
        conn.execute(schema_file)  


# SEND DATA


engine =  sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}')
with engine.begin() as conn:
    
    conn.execute("SET FOREIGN_KEY_CHECKS = 0;")
    
    genes = pd.read_csv('../genes_to_db_new.csv', sep='\t')
    #genes_col_trans = ['gene_stable_id', 'gene_description', 'gene_end', 'gene_start', 'gene_name', 'hgnc_id']
    genes_col_trans = {
        'Gene stable ID': 'gene_stable_id', 
        'Gene description': 'gene_description',
        'Chromosome/scaffold name': 'chromosome/scaffold', 
        'Gene start (bp)': 'gene_start', 
        'Gene end (bp)': 'gene_end', 
        'Gene name': 'gene_name', 
        'HGNC ID': 'hgnc_id'
    }
    send_to_db_with_delay(conn, genes, 'Genes', genes_col_trans, primary_key='gene_stable_id', chunksize=100)
    

    proteins = pd.read_csv('../proteins_to_db.csv', sep='\t')
    send_to_db_with_delay(conn, proteins, 'Proteins')
    
    seq = pd.read_csv('../sequence_predictions/OUT_ALL_CLEAN.csv')
    seq_trans = {x: x for x in seq.columns}
    seq_trans['Initial Label'] = 'Initial_label'
    seq_trans['Sequence'] = 'sequence'
    del seq_trans['AU.1']
    send_to_db_with_delay(conn, seq, 'sequence', seq_trans)
    
    sno = pd.read_csv('../sequences/snoRNA_rt-489815.tsv', sep='\t')
    sno_trans = {
        'external_id' : 'family', 
        'feature_start' : 'start_pos',
        'feature_end' : 'end_pos',
        'seq_short' : 'sequence',
        'insdc_id' : 'chr_genbank_id',
        'description' : 'description',
    }
    send_to_db_with_delay(conn, sno, 'snoRNAs', sno_trans)
    
    rrna = pd.read_csv('../sequences/rRNA_rt-489815.tsv', sep='\t')
    rrna_trans = {
        'external_id' : 'family', 
        'feature_start' : 'start_pos',
        'feature_end' : 'end_pos',
        'seq_short' : 'sequence',
        'insdc_id' : 'chr_genbank_id',
        'description' : 'description',
    }
    send_to_db_with_delay(conn, rrna, 'rRNAs', rrna_trans)
    
    trna = pd.read_csv('../sequences/tRNA_rt-489815.tsv', sep='\t')
    trna_trans = {
        'external_id' : 'family', 
        'feature_start' : 'start_pos',
        'feature_end' : 'end_pos',
        'seq_short' : 'sequence',
        'insdc_id' : 'chr_genbank_id',
        'description' : 'description',
    }
    send_to_db_with_delay(conn, trna, 'tRNAs', trna_trans)
    
    stem = pd.read_csv('../out_stem_human.csv', sep='\t')
    stem_trans = {
        '1' : 'stem_accession', 
        '2' : 'stem_id',
        '4' : 'description',
        '5' : 'sequence',
        '6' : 'cc',
        'SQ': 'seq_description' 
    }
    send_to_db_with_delay(conn, stem, 'miRNAs_stem', stem_trans)
    
    trfs = pd.read_csv('../final_mintbase_tRFdb_toDB.csv', sep='\t')
    send_to_db_with_delay(conn, trfs, 'tRFs')
    
    fnc = pd.read_csv('../Function/new_out_function_descriptions.tsv', sep='\t')
    fnc_trans = {'Function ID': 'Function_ID', 'Function Description' : 'Function_description'}
    send_to_db_with_delay(conn, fnc, 'Function_descriptions', fnc_trans)
    
    fnc_mat = pd.read_csv('../Function/new_out_function_matches.tsv', sep='\t')
    fnc_mat_trans = {'Entry': 'uniprot_entry', 'Function Description ID': 'Function_ID', 'Function Type' : 'function_type_number'}
    send_to_db_with_delay(conn, fnc_mat, 'Protein_Function', fnc_mat_trans, chunksize=1000)
    
    mirna_mat = pd.read_csv('../out_mirna_mature-mature.csv', sep='\t')
    mirna_mat_trans = {
        'MIMAT_ID': 'mature_accession',
        'CodeX': 'mature_id',
        'Sequence': 'mature_sequence',
        'method?': 'evidence',
        'Similarity': 'similarity',
        'text?': 'experiment',

    }
    send_to_db_with_delay(conn, mirna_mat, 'miRNAs_mature', mirna_mat_trans)
    
    genes_proteins = pd.read_csv('../genes_proteins_to_db.csv', sep='\t')
    genes_proteins_trans = {
        "Gene stable ID": "gene_stable_id",
        "uniprot_entry": "protein_uniprot_entry"
    }
    send_to_db_with_delay(conn, genes_proteins, 'Gene_Protein', genes_proteins_trans)

    mirnas_mature_genes = pd.read_csv('../mirnas_mature_genes.csv', sep='\t')
    send_to_db_with_delay(conn, mirnas_mature_genes, 'miRNA_mature_Genes', chunksize=1000)


# engine =  sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}')
print("Linking keys with sequence")
with engine.begin() as conn:
    multi_update = """
CREATE INDEX seq_index ON sequence(sequence(100));

UPDATE miRNAs_mature 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            miRNAs_mature.mature_sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;

UPDATE miRNAs_stem 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            miRNAs_stem.sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;

UPDATE rRNAs 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            rRNAs.sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;


UPDATE snoRNAs 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            snoRNAs.sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;

UPDATE tRFs 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            tRFs.sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;


UPDATE tRNAs 
SET 
    sequenceid = (SELECT 
            sequence_id
        FROM
            sequence
        WHERE
            tRNAs.sequence = sequence.sequence
        LIMIT 1)
WHERE
    sequenceid IS NULL;

UPDATE miRNAs_stem SET length = LENGTH(sequence);

CREATE INDEX mature_id_idx ON miRNAs_mature(mature_id);
CREATE INDEX gene_name_idx ON Genes(gene_name);

"""
    for update in multi_update.split(';'):
        if update.isspace():
            continue

        update += ';'
        update = update.strip()
        try:
            conn.execute(update)
        except Exception as e:
            print("Index already exist", e)

# os.chdir(os.path.dirname(__file__))
print("Linking mature - stem")
with engine.begin() as conn:
    print("creating temporary table")
    link = pd.read_csv("../miRNAdat_accessions.csv", sep=';')
    link.to_sql("mature_stem_link_temp", conn, chunksize=100, method='multi', if_exists='replace')

    print("Creating indexes")
    try:
        conn.execute("CREATE INDEX aid ON mature_stem_link_temp(Accession(15))")
    except:
        print("Index already exist")

    try:
        conn.execute("CREATE INDEX stem_ac_idx ON miRNAs_stem(stem_accession(15))")
    except:
        print("Index already exist")

    print("Linking keys")
    conn.execute("""
UPDATE miRNAs_mature 
SET 
    stemid = (SELECT 
            miRNAstem_id
        FROM
            miRNAs_stem
        WHERE
            miRNAs_stem.stem_accession = (
                SELECT AC
                FROM mature_stem_link_temp
                WHERE Accession = miRNAs_mature.mature_accession
                LIMIT 1
            )
        LIMIT 1)
WHERE
    stemid IS NULL;
"""
    )

    print("Droping temporaries")
    conn.execute("DROP TABLE mature_stem_link_temp;")
    
    conn.execute("SET FOREIGN_KEY_CHECKS = 1;")

