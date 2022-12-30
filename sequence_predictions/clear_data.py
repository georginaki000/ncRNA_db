import pandas as pd
import numpy as np
import os
import shutil

os.chdir(os.path.dirname(__file__))

def clean_sequence_file(filename):

    dirty_df = pd.read_csv(filename, sep=',')

    if "Initial Label" in dirty_df.columns:
        print(f"{filename} OK, ignore")
        return

    print(f"Cleaning: {filename}")

    # copy original file to backup
    backup_filename = "original_"+filename

    print(f"\tBack-uping file to {backup_filename}")
    shutil.copyfile(filename, backup_filename)


    if "Label" in dirty_df.columns:
        dirty_df.rename(columns={"Label" : "Initial Label"}, inplace=True)
    elif "Initial Labe" in dirty_df:
        dirty_df.rename(columns={"Initial Labe" : "Initial Label"}, inplace=True)
    
    else:

        # split the Sequence part to get the initial label and sequence
        intial_label = dirty_df["Sequence"].str.split(' ').str[:-1].str.join(' ').str.lstrip("> ")
        sequence = dirty_df["Sequence"].str.split(' ').str[-1]

        dirty_df["Initial Label"] = intial_label
        dirty_df["Sequence"] = sequence

        # rearrange the columns
        other_cols = list(dirty_df.columns.values[:-1])
        other_cols.remove("index")
        rearranged_columns = ["Initial Label"] + other_cols
        
        dirty_df = dirty_df[rearranged_columns]

    print(f"\tRewriting cleaned file to {filename}")
    dirty_df.to_csv(filename, sep=',', index=False)


# dirty_files = ["sequence_24_predicted.csv", "sequence_25_predicted.csv", "sequence_26_predicted.csv"]

# for dirty_file in dirty_files:
#     clean_sequence_file(dirty_file)

sequence_files = [filename for filename in os.listdir() if os.path.isfile(filename) and filename.startswith("sequence") and filename.endswith("csv")]

for sequence_file in sequence_files:
    clean_sequence_file(sequence_file)

# get unique Initial Lables
unique_initial_labels = set()
for sequence_file in sequence_files:
    df = pd.read_csv(sequence_file, sep=',')

    unique_initial_labels.update(df["Initial Label"].dropna().unique())


all_df = pd.concat([pd.read_csv(seq_file, sep=',') for seq_file in sequence_files])

all_df.dropna(subset=["Initial Label"], inplace=True)

print(f"All len {len(all_df)}")

# print("Unique Inital Labels:")
# print(unique_initial_labels)
# for label in unique_initial_labels:
#     print(label)

with open("unique_initial_labels.txt", "w") as file:
    for label in unique_initial_labels:
        file.write(str(label))
        file.write("\n")



keeps = {}

for label in unique_initial_labels:

    new_label = None

    if "mir" in label or "microRNA" in label:
        new_label = "hairpin" # go back to hairpin
    
    elif "nucleolar" in label:
        new_label = "snoRNA"

    elif "ribosomal" in label or "rRNA" in label:
        new_label = "rRNA"
        
    elif "transfer" in label or "tRNA" in label:
        new_label = "tRNA"

    elif "trf" in label or "mature" in label or "hairpin" in label:
        new_label = label

   
    if new_label is None or str(label) == 'nan':
        # remove those columns
        all_df = all_df[all_df["Initial Label"] != label]
    
    else:
        # rename label
        #print(f"{label} -> {new_label}")
        keeps[label] = new_label
        all_df.replace({label : new_label}, inplace=True)
    

print(f"All len after renames: {len(all_df)}")
print(f"labels kept: {len(keeps)}")

new_labels = sorted(list(set(keeps.values())))
print(f"transformed labels dict: {len(new_labels)}")
print(new_labels)

new_labels_from_all = sorted(list(all_df["Initial Label"].unique()))
print(f"df labels dict: {len(new_labels_from_all)}")
print(new_labels_from_all)

assert new_labels == new_labels_from_all

# clear non human and mistakes
with open("hairpin_fa_mistakes.txt", 'r') as mf:
    bad_sequences = [seq.strip() for seq in mf]

print(f"Bad sequences: {len(bad_sequences)}")

pl = len(all_df)
all_df = all_df[~all_df["Sequence"].isin(bad_sequences)]
al = len(all_df)
print(f"All len after bad sequence cleanup: {al} ({pl-al} sequences removed)")

# clear values
data_columns = all_df.columns.values[2:]
for column in data_columns:
    print(f"Cleaning column {column}")
    all_df[column] = pd.to_numeric(all_df[column], errors="coerce")
    col = all_df[column]
    col_max = col[np.isfinite(col)].max()
    col_min = col[np.isfinite(col)].min()
    col_mean = col[np.isfinite(col)].mean()
    all_df[column].replace([np.inf], col_max, inplace=True)
    all_df[column].replace([-np.inf], col_min, inplace=True)
    all_df[column].fillna(col_mean, inplace=True)


all_df.drop(columns=["index"], inplace=True)

all_df.to_csv("OUT_ALL_CLEAN.csv", sep=',', index=False)


with open("labels_kept.txt", "w") as file:
    for label, new_name in keeps.items():
        file.write(f"{label}\t{new_name}\n")


no_bad_cols = all_df.drop(columns=["Sequence", "Mature", "pre-miRNA", "tRNA", "rRNA", "snoRNA", "trfs", "pseudo-hairpins", "Random"])
cols = no_bad_cols.columns[1:]

gb = no_bad_cols.groupby(["Initial Label"])
stats = gb.agg([np.min, np.max, np.mean])
#stats = gb.mean()
print(stats["AA"])

with open("OUT_STATS_LINE.txt", "w") as f:
    f.write(stats.to_string())

with open("OUT_STATS_STACKED.txt", "w") as f:
    for col in cols:
        f.write(col + "\n")
        f.write(stats[col].to_string())
        f.write("\n\n")
