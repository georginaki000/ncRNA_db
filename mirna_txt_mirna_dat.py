import pandas as pd

mirna_txt = 'mirna.txt'
miRNA_dat = 'miRNA.dat'

mirna_txt_df = pd.read_csv(mirna_txt, header=None, sep='\t')


# read mirna.dat

data = []

with open(miRNA_dat, 'r') as mirna_dat:
    new = []
    for line in mirna_dat.readlines():
        line = line.strip()

        line_split_data = line.split(' ' * 3)
        if line.startswith('AC'):
            new = []
            new.append(line_split_data[1][:-1]) # skip ;
        
        elif line.startswith('SQ'):
            new.append(line_split_data[1])

        elif line.startswith('//'):
            assert(len(new) == 2)
            data.append(new)


mirna_dat_df = pd.DataFrame(data, columns = ['AC', 'SQ'])

# print(mirna_dat_df)

joined_data_df = mirna_txt_df.merge(mirna_dat_df, how='inner', left_on=1, right_on='AC')
joined_data_df.drop(columns=['AC'], inplace = True)

joined_data_df.to_csv('out_mirnatxt_mirnadat.csv', index=False, sep='\t')

print(joined_data_df['SQ'])
stem = joined_data_df[joined_data_df[4].str.contains("Homo") | joined_data_df[4].str.contains("Homo") ]
print(len(joined_data_df), len(stem))
stem.to_csv('out_stem_human.csv', index=False, sep='\t')


