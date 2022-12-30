import pandas as pd
import numpy as np
import os
from pandas.core.dtypes.missing import notna
import sqlalchemy


MERGE_LABEL = 'Fragment sequence'

foldername = 'tRF-1'

mintbase_new = "mintbase_new"
trfdb        =  os.path.join(foldername, "trfdb_csv_result.csv")

os.chdir(os.path.dirname(__file__))

mintbase_new_names = ['Type_mintbase', 'MINTbase Unique ID (sequence derived)', 'Unique tRNA name', 'tRNA number', 
    'Amino acid and anticodon', 'Chromosome', 'Chromosome strand', 'Chromosome start position', 
    'Chromosome end position', 'Start position relative to start of mature tRNA', 
    'End position relative to start of mature tRNA', 'Fragment sequence', 'Fragment length', '']

mintbase_new_df = pd.read_csv(mintbase_new, header=None, sep='\t', comment='#', names=mintbase_new_names, 
                                            skip_blank_lines=True, skipinitialspace=True, usecols=mintbase_new_names[:-1]) # skip broken last column

print('mintbase length:', len(mintbase_new_df))

mintbase_new_no_duplicates = mintbase_new_df.drop_duplicates(subset=MERGE_LABEL)
print('mintbase no duplicates length:', len(mintbase_new_no_duplicates))

# print(len(mintbase_new_df[mintbase_new_df['Fragment length'] > 60]))
# print(mintbase_new_df.iloc[0])

def read_trfdb_seg(filename):

    # trfdb =  os.path.join(folder_name, "trfdb_csv_result.csv")

    trfdb_df = pd.read_csv(filename, header=0, sep=',', skipinitialspace=True)

    # clear last space on sequence
    trfdb_df['tRF Sequence'] = trfdb_df['tRF Sequence'].str.strip()

    # print(trfdb_df)
    # print(trfdb_df.iloc[1])

    rel_start_end = pd.DataFrame(trfdb_df['tRF Map Positions'].str.split(' - ').apply(lambda x : pd.Series([int(st.split(':')[1]) for st in x]))).rename(columns={0:'Start', 1:'End'})

    trfdb_df[['Relative Start', 'Relative End']] = rel_start_end

    trfdb_df[['tRNA number', 'Amino acid and anticodon']] = trfdb_df['tRNA Name'].str.split('-', expand=True)
    trfdb_df['tRNA number'] = trfdb_df['tRNA number'].str.split('.', expand=True)[1]
    trfdb_df['Fragment Length'] = trfdb_df['tRF Sequence'].str.len()

    trfdb_df[['Chromosome Start', 'Chromosome End']] = trfdb_df['tRNA Gene Co-ordinates'].str.split('-').apply(lambda x : pd.Series([int(x[1]), int(x[2])]))

    diff = trfdb_df['Chromosome End'] - trfdb_df['Chromosome Start']

    trfdb_df['Chromosome End'] +=  np.sign(diff) * trfdb_df['Fragment Length']

    trfdb_df['Chromosome strand'] = diff.apply(lambda x : '+' if x >= 0 else '-')

    # get Chromosome
    trfdb_df['Chromosome'] = trfdb_df['tRNA Name'].str.split('.').str.get(0).str.lstrip('chr')



    # print(trfdb_df.iloc[0])
    # print("-------------")

    trfdb_df.rename(columns= {'tRF Sequence'     : MERGE_LABEL,
                            'Chromosome Start' : 'Chromosome start position',
                            'Chromosome End'   : 'Chromosome end position',
                            'Relative Start'   : 'Start position relative to start of mature tRNA',
                            'Relative End'     : 'End position relative to start of mature tRNA'}, inplace=True)


    return trfdb_df


#result_df = pd.concat([trfdb_df, start_end], axis=1)

# print(trfdb_df.iloc[3])

print("-------------")

trfdb_segments = [read_trfdb_seg(os.path.join('tRF-1', 'trfdb_csv_result.csv')),
                  read_trfdb_seg(os.path.join('tRF-3', 'trfdb3_csv_result.csv')),
                  read_trfdb_seg(os.path.join('tRF-5', 'trfdb5_csv_result.csv'))]


print(trfdb_segments[0].head())

trfdb_segments_concated = pd.concat(trfdb_segments)

print('concated sum:', len(trfdb_segments_concated))


# joined_data_concated = pd.concat([mintbase_new_df, trfdb_segments_concated], keys=[MERGE_LABEL], axis=0, join='outer', sort=False)
# print('joined inner length:', len(joined_data_concated))
# joined_data_concated.to_csv(output_name, sep='\t', index=False, na_rep ='NA') 

merged_data = pd.merge(mintbase_new_df, trfdb_segments_concated, how='outer', on=MERGE_LABEL)

# print(merged_data.columns)

print('merge length:', len(merged_data))

output_name = 'out_'+ mintbase_new + '_' + foldername + '.csv'
merged_data.to_csv(output_name, sep='\t', index=False, na_rep='NA')



# merged_data_no_duplicates = pd.merge(mintbase_new_no_duplicates, trfdb_segments_concated, how='outer', on=MERGE_LABEL)
# print('no dup merged length', len(merged_data_no_duplicates))

# output_name = 'out_'+ mintbase_new + '_' + foldername + '_no_duplicates_' +  '.csv'
# merged_data_no_duplicates.to_csv(output_name, sep='\t', index=False, na_rep='NA')


# Create final filtered and merged matadframe
final_df = pd.DataFrame()

final_df['mintbase_ID'] = merged_data['MINTbase Unique ID (sequence derived)']
final_df['alternate_ID']   = merged_data['tRF ID']
final_df['chromosome'] = merged_data['Chromosome_x'].fillna(merged_data['Chromosome_y'])
final_df['start_pos_chr']  = merged_data['Chromosome start position_x'].fillna(merged_data['Chromosome start position_y'])
final_df['end_pos_chr']    = merged_data['Chromosome end position_x'].fillna(merged_data['Chromosome end position_y'])
final_df['start_pos_tRNA']    = merged_data['Start position relative to start of mature tRNA_x']
final_df['end_pos_tRNA']    = merged_data['End position relative to start of mature tRNA_x']
final_df['sequence']   = merged_data['Fragment sequence']
final_df['trfdb_id']   = merged_data['tRF ID']
final_df['tRF_type']   = merged_data['Type_mintbase'].fillna(merged_data['Type'])


# clear not int positions
print('before: ', len(final_df))

final_df = final_df[pd.to_numeric(final_df['start_pos_chr'], errors='coerce').notnull()]
final_df = final_df[pd.to_numeric(final_df['end_pos_chr'], errors='coerce').notnull()]
final_df = final_df[pd.to_numeric(final_df['start_pos_tRNA'], errors='coerce').notnull()]
final_df = final_df[pd.to_numeric(final_df['end_pos_tRNA'], errors='coerce').notnull()]
final_df = final_df[pd.to_numeric(final_df['chromosome'], errors='coerce').notnull()]

print('after:', len(final_df))




#unique_tRF_types = final_df['tRF_type'].unique()
# print(unique_tRF_types)


# Uncomment to make replaces
final_df.drop(columns=["alternate_ID"], inplace=True)
final_df['tRF_type'].replace({'trf-1' : "i-tRF", 'trf-3' : "3'-tRF", 'trf-5' : "5'-tRF"}, inplace=True)


final_df.to_csv('final_mintbase_tRFdb_toDB.csv', sep='\t', index=False, na_rep='NA')

# exit()
# DB_USER = "diamantop"
# DB_PASSWORD = "12345678"
# DB_HOSTNAME = "pez.insybio.com"
# DB_PORT = "3306"
# DB_NAME = "diamantop_ncrnas"
# DB_TABLE = "tRFs"



# engine = sqlalchemy.create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}')

# final_df.to_sql(DB_TABLE, engine, index=False, if_exists='append', chunksize=20)

# # close connections
# engine.dispose()