import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

if not os.path.isfile("uniprot-data.csv"):
    uniprot_data = pd.read_excel("uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.xlsx", dtype=str)
    uniprot_data.to_csv("uniprot-data.csv", sep='\t', index=False)
else:
    uniprot_data = pd.read_csv("uniprot-data.csv", sep='\t', dtype=str)

mart_data = pd.read_csv("RFAM/mart_export.txt", sep='\t')
proteins = pd.read_csv("proteins_to_db.csv", sep='\t')
genes = pd.read_csv("genes_to_db_new.csv", sep='\t')


# create new uniprot link csv genes names
# keep columns
uniprot_link_columns = ["Entry", "Gene names"]
uniprot_link_data = uniprot_data[uniprot_link_columns]

uniprot_link_data['Gene names'] = uniprot_link_data['Gene names'].astype(str)

print(f"Read {len(uniprot_link_data)} rows")

# split the gene names 
# https://sureshssarda.medium.com/pandas-splitting-exploding-a-column-into-multiple-rows-b1b1d59ea12e
link_df = pd.DataFrame(uniprot_link_data["Gene names"].str.split(" ").tolist(), index=uniprot_link_data["Entry"], dtype=str).stack()

link_df = link_df.reset_index([0, "Entry"])
link_df.columns = ["uniprot_entry", "Gene name"]

link_df.to_csv("gene_proteins_link.csv", sep='\t', index=False)

# map to gene stable ids
genes_link_columns = ["Gene stable ID", "Gene name"]
genes_link_df = genes[genes_link_columns]

final_link_df = pd.merge(link_df, genes_link_df, how='inner', on="Gene name")
final_link_df.drop_duplicates(inplace=True)

print(f"Total links {len(final_link_df)}")

final_link_df.to_csv("genes_proteins_to_db.csv", sep='\t', index=False)

uniq_uniprot_entries = set(final_link_df["uniprot_entry"])
proteins_mapped = len(uniq_uniprot_entries & set(proteins["uniprot_entry"]))
print(f"Mapped {proteins_mapped} / {len(proteins)} ({proteins_mapped / len(proteins) * 100:5.2f}%) of proteins")


uniq_genes = set(final_link_df["Gene stable ID"])
genes_mapped = len(uniq_genes & set(genes["Gene stable ID"]))
print(f"Mapped {genes_mapped} / {len(genes)} ({genes_mapped / len(genes) * 100:5.2f}%) of genes")