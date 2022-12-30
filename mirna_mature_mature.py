import pandas as pd

mirna_mature = "mirna_mature.txt"
mature_fa    = "mature.fa"

# TODO:                                                                                                    USE THIS FOR OUTPUT         v
mirna_mature_df = pd.read_table(mirna_mature, header=None, names=['MIRNA_MATURE#', 'CodeX', 'CodeY', 'MIMAT_ID', 'method?', 'text?', 'Similarity', 'number'])

# print(mirna_mature_df)

# Workaround to deal with 2-line entries
data = []

with open(mature_fa, 'r') as fp:
    
    while True:
        info = fp.readline()
        seq  = fp.readline() 

        if not (info or seq):
            break
        
        info = info.replace('>', '').strip()
        seq  = seq.strip()
        
        entry = info.split()
        entry.append(seq)

        data.append(entry)


mature_fa_df = pd.DataFrame(data, columns=['ID', 'MIMAT_ID', 'Species', 'Species 2', 'Code', 'Sequence'])
# print(mature_fa_df)


joined_df = mirna_mature_df.join(mature_fa_df.set_index('MIMAT_ID'), on='MIMAT_ID', how='right')

# only_human_species = joined_df[joined_df['Species'].str.match('Homo')]

only_human_codex   = joined_df[joined_df['CodeX'].str.startswith('hsa')]

only_human_codex.to_csv('out_mirna_mature-mature.csv', sep='\t', index=False, na_rep='NA')