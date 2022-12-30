from operator import concat
from numpy import mat
import pandas as pd
import os

# Change directory to the scripts directory
os.chdir(os.path.dirname(__file__))

FUNCTIONS_FILE_EXCEL = "functions_filtered_new.xlsx"

FUNCTION_SEPARATOR = "; "

function_df = pd.read_excel(FUNCTIONS_FILE_EXCEL)

keeps = [
    "Entry", 
    "Gene ontology (biological process)", 
    "Gene ontology (cellular component)",
    "Gene ontology (GO)",
    "Gene ontology (molecular function)",
    "Gene ontology IDs"
]

filtered = function_df[keeps]
# tropos 1
filtered.to_csv("out_function_keep_cols.csv", sep='\t', index=False)

# print(filtered.head())

# tropos 2
# for unique_field in keeps[1:]:
#     unique_functions = function_df[unique_field].split(";").unique()

#     unique_functions_dict = {function_string : inc_id for inc_id, function_string in enumerate(unique_functions)}

#     id_col_name = f"ID ({unique_field})".replace('(', '_').replace(')', '_').replace(' ', '')

#     unique_functions_dict_df = pd.DataFrame(unique_functions_dict.items(), columns = (id_col_name, unique_field))
#     unique_functions_dict_df.to_csv(f"unique_field_{id_col_name}.csv", sep='\t')

#     function_df[id_col_name] = function_df[unique_field].map(unique_functions_dict)

# function_df.to_csv(f"out_function_all_joined.csv", sep='\t', index=False)

# -------
count = 0
matches = []
function_ids = {}
function_type_numbers = {}

for function_type_id, unique_field in enumerate(keeps[1:]):
    df = function_df[[keeps[0], unique_field]]
    function_type_numbers[function_type_id] = unique_field

    # print(unique_field)

    for index, df_row in df.iterrows():
        
        if type(df_row[unique_field]) is not str: continue

        entry_functions = df_row[unique_field].split(FUNCTION_SEPARATOR)
        entry = df_row[keeps[0]]

        for entry_function in entry_functions:
            if entry_function not in function_ids:
                function_ids[entry_function] = count
                count += 1
            
            # A funciton match: Entry, Function Description FK, function type
            match_tuple = (entry, function_ids[entry_function], function_type_id)
            matches.append(match_tuple)

        #print(f"{index} => {entry_functions}")


function_ids_list = [(f_id, f_desc) for f_desc, f_id in function_ids.items()]

matches_df = pd.DataFrame(matches, columns=("Entry", "Function Description ID", "Function Type Number"))
function_ids_df = pd.DataFrame(function_ids_list, columns=("Function ID", "Function Description"))
function_type_numbers_df = pd.DataFrame(function_type_numbers.items(), columns=("Function Type Number", "Function Type"))

function_type_numbers_df.replace({"Function Type": {
    'Gene ontology (biological process)' : 'Biological Process',
    'Gene ontology (cellular component)' : 'Cellural Component',
    'Gene ontology (GO)' : 'GO',
    'Gene ontology (molecular function)' : 'Molecular Function',
    'Gene ontology IDs' : 'IDs'
    }}, inplace=True)

matches_df = matches_df.merge(function_type_numbers_df, how='inner', on="Function Type Number")
matches_df.to_csv("new_out_function_matches.tsv", sep='\t', index=False)
function_ids_df.to_csv("new_out_function_descriptions.tsv", sep='\t', index=False)
function_type_numbers_df.to_csv("new_out_function_type_numbers.tsv", sep='\t', index=False)