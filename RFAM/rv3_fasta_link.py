import pandas as pd
import os

linking_file = "mart_export (1).txt"

def read_linking_file():
    linking_df = pd.read_csv(linking_file, sep = '\t', engine='c')
    
    linking_df.dropna(inplace=True)
    
    return linking_df


def read_fasta(path):
    
    # Workaround to deal with 2-line entries
    data = []

    with open(path, 'r') as fp:
        
        while True:
            info = fp.readline()
            seq  = fp.readline() 

            if not (info or seq):
                break
            
            info = info.replace('>', '').strip()
            seq  = seq.strip()
            
            id_stripped = info.split('_')[0]

            #entry = info.split()
            entry = [id_stripped, info]
            entry.append(seq)

            data.append(entry)


    fasta_df = pd.DataFrame(data, columns=['ID .fasta', 'All Data .fasta', 'Sequence'])

    return fasta_df

def read_fa(path):
    # Workaround to deal with 2-line entries
    data = []

    with open(path, 'r') as fp:
        
        while True:
            info = fp.readline()
            seq  = fp.readline() 

            if not (info or seq):
                break
            
            info = info.replace('>', '').strip()
            seq  = seq.strip()
            
            id_stripped = info.split('.')[0]

            #entry = info.split()
            entry = [id_stripped, info]
            entry.append(seq)

            data.append(entry)


    fa_df = pd.DataFrame(data, columns=['ID .fa', 'All Data .fa', 'Sequence'])

    return fa_df
# --------

linker = read_linking_file()

# print(linker)

fas = []
fa_all = []

for rel_path in os.listdir('./fasta_files_RFAM'):
    if not rel_path.endswith('.fa'):
        continue

    
    full_rel_path = os.path.join('.', 'fasta_files_RFAM', rel_path)
    print(full_rel_path)
    fa = read_fa(full_rel_path)
    fa['fa origin file'] = rel_path

    fa_all.append(fa)

    merged = linker.merge(fa, how = 'inner', left_on = 'European Nucleotide Archive ID', right_on = 'ID .fa')
    
    fas.append(merged)
    
fas_df = pd.concat(fas)
fas_df_human = fas_df[fas_df['All Data .fa'].str.contains('Homo sapiens|Human')]

fas_df.reset_index(inplace = True, drop = True)
fas_df_human.reset_index(inplace = True, drop = True)

fas_df.to_csv('RFXXXXX.fa_matches_all.csv', sep=';')
fas_df_human.to_csv('RFXXXXX.fa_matches_human.csv', sep=';')

print(fas_df)
print(fas_df_human)

fa_all_df = pd.concat(fa_all)
fa_all_df.reset_index(inplace = True, drop = True)

print('ALL .fa :', len(fa_all_df))

rfams = []
fasta_all = []
# --- link linker - rfam
for rel_path in os.listdir('./RFAM EXPERT'):
    if not rel_path.endswith('.fasta'):
        continue

    full_rel_path = os.path.join('.', 'RFAM EXPERT', rel_path)
    # print(full_rel_path)

    fasta = read_fasta(full_rel_path)
    fasta_all.append(fasta)
    # print(fasta)
    # print(fasta['Sequence'].apply(len).mean()) 
    merged = linker.merge(fasta, how = 'inner', left_on = 'RNAcentral ID', right_on = 'ID .fasta')
    rfams.append(merged)
    # print(merged)

rfams_df = pd.concat(rfams)


print("------------")
print(rfams_df)


fasta_all_df = pd.concat(fasta_all)
fasta_all_df.reset_index(inplace = True, drop = True)

print('ALL .fasta :', len(fasta_all_df))

merged_on_sequence = fa_all_df.merge(fasta_all_df, how='inner', on = 'Sequence')

print("Merged on sequence length: ", len(merged_on_sequence))

merged_on_sequence.to_csv('sequence_merged.csv', sep=';')

merged_on_sequence_both_human = merged_on_sequence[merged_on_sequence['All Data .fa'].str.contains('Homo sapiens|Human') &
                                              merged_on_sequence['All Data .fasta'].str.contains('Homo sapiens|Human')]


print("Merged on sequence-both_human: ", len(merged_on_sequence_both_human))


merged_on_sequence_both_human.to_csv('sequence_merged_both_human.csv', sep=';')