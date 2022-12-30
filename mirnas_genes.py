import os
import pandas as pd

os.chdir(os.path.dirname(__file__))

filenames = [os.path.join("mirnas_genes", filename) for filename in os.listdir("mirnas_genes") if filename.startswith("miRNA_gene_score")]

print(f"Concating {len(filenames)} files")
all_df = pd.concat([pd.read_csv(filename, sep='\t') for filename in filenames])
all_df.columns = ["mature_id", "gene_name", "score"]

print(len(all_df))
all_df.sort_values(by=['score'], ascending=False)
all_df.drop_duplicates(subset=("mature_id", "gene_name"), inplace=True)

all_df = all_df[all_df['score'] > 0]
print(len(all_df))

all_df.to_csv("mirnas_mature_genes.csv", sep='\t', index=False)