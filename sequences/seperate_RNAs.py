import pandas as pd
import os

from pandas.core.algorithms import unique

os.chdir(os.path.dirname(__file__))

rnas_filename = 'rt-489815.tsv'


rnas_df = pd.read_csv(rnas_filename, sep='\t')


classes = {'tRNA': 'tRNA', 'rRNA' : 'rRNA', 'snoRNA' : 'SNO', 'microRNA' : 'mir'}

for classname, substr in classes.items():
    col_filter = rnas_df['optional_id'].str.lower().str.contains(substr.lower())
    out_df = rnas_df[col_filter]

    print(f"{classname} => {len(out_df)}")
    out_df.to_csv('_'.join([classname, rnas_filename]), index=False, sep='\t')


# print(rnas_df.head())

# unique_desc = rnas_df['optional_id'].unique()
# print(unique_desc)
# print(len(unique_desc))