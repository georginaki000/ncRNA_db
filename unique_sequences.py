import pandas as pd
import os
from pandas.core.algorithms import unique

os.chdir(os.path.dirname(__file__))

# fa files
def fa_file_seq(filename):
    seqs = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('>'):
                seqs.append(line)

    
    return set(seqs)

fa_df = pd.DataFrame(list(fa_file_seq("mature.fa")), columns=["Sequence"])
fa_df["Type"] = "mature"
print("fa_df: ", fa_df.iloc[0].isnull().sum())
# all = fa_file_seq("mature.fa")
# print(len(all))

hairpin_df = pd.DataFrame(list(fa_file_seq("hairpin.fa")), columns=["Sequence"])
hairpin_df["Type"] = "hairpin"
print("hairpin_df: ", hairpin_df.iloc[0].isnull().sum())
# all = all.union(fa_file_seq("hairpin.fa"))
# print(len(all))


rnacentral_df = pd.read_csv("./sequences/rt-489815.tsv", sep='\t')
print(len(rnacentral_df))
rnacentral_seq = list(rnacentral_df["seq_long"].unique())
print("rnacentral_df: ", rnacentral_df["seq_long"].isnull().sum())

# all = all.union(set(rnacentral_seq))
# print(len(all))
# mintabase

mintbase_new_names = ['Type_mintbase', 'MINTbase Unique ID (sequence derived)', 'Unique tRNA name', 'tRNA number', 
    'Amino acid and anticodon', 'Chromosome', 'Chromosome strand', 'Chromosome start position', 
    'Chromosome end position', 'Start position relative to start of mature tRNA', 
    'End position relative to start of mature tRNA', 'Fragment sequence', 'Fragment length', '']

mintbase_new_df = pd.read_csv("mintbase_new", header=None, sep='\t', comment='#', names=mintbase_new_names, 
                                            skip_blank_lines=True, skipinitialspace=True, usecols=mintbase_new_names[:-1]) # skip broken last column
mintbase_new_df["Type"] = "trf"
print("mintbase: ", mintbase_new_df["Fragment sequence"].isnull().sum())
# mintbase_new_seq = set(mintbase_new_df['Fragment sequence'].unique())

# all = all.union(mintbase_new_seq)

# print(len(all))
# trfdb

trfdb_segments = [pd.read_csv(os.path.join('tRF-1', 'trfdb_csv_result.csv') , skipinitialspace=True),
                  pd.read_csv(os.path.join('tRF-3', 'trfdb3_csv_result.csv'), skipinitialspace=True),
                  pd.read_csv(os.path.join('tRF-5', 'trfdb5_csv_result.csv'), skipinitialspace=True)]


trfdb_segments_concated = pd.concat(trfdb_segments)
print("trfd: ", trfdb_segments_concated.iloc[0].isnull().sum())
trfdb_segments_concated["Type"] = "trf"


# trfdb_seq = set(trfdb_segments_concated['tRF Sequence'].unique())


# all = all.union(trfdb_seq)
# print(len(all))


all_df = pd.concat([
    fa_df,
    hairpin_df,
    rnacentral_df[["seq_short", "description"]].rename(columns={"seq_short" : "Sequence", "description" : "Type"}),
    mintbase_new_df[["Fragment sequence", "Type"]].rename(columns={"Fragment sequence" : "Sequence"}),
    trfdb_segments_concated[["tRF Sequence", "Type"]].rename(columns={"tRF Sequence" : "Sequence"})
    ],
    ignore_index=True,
    names = ["Sequence", "Type"]
)

all_df.drop_duplicates(inplace=True)
print("Before: ", len(all_df))
all_df.dropna(inplace=True)
print("after: ", len(all_df))

all_df = all_df[all_df["Sequence"] != "None"]

print(all_df.head())
print("all_df: ", all_df["Sequence"].isnull().sum())

all_df.to_csv("unique_sequence_with_origin.tsv", sep='\t', index=False)

# # write to files
# with open("UNIQUE_SEQUENCES.txt", 'w') as f:

#     for seq in all:
#         print(seq, file=f)
