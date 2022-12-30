import pandas as pd

df = pd.read_csv("mirna_mature.txt", sep='\t', header=None)

b = df[df.columns[1]]

b = b[b.str.startswith("hsa")]

b.to_csv("mirna_humans.csv", index=False, header=False)