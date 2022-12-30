import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.stats
import statsmodels.stats.multitest

os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "histograms"
INPUT_FILENAME = "OUT_ALL_CLEAN.csv"

DISTINCT_THRESHOLD = 10
# create output dir
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

data = pd.read_csv(INPUT_FILENAME, sep=',', low_memory=False)
sequence_types = list(data["Initial Label"].unique())

print(sequence_types)

trfs = data[data["Initial Label"] == "trf"]

data_columns = data.columns.values[10:]

COLOR_PALETTE = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

kruskal_data = []
MW_data = []
KS_data = []
# Kruskal wallis
ZERO_THRESHOLD = 1e-5
for column in data_columns:
    curr_col_mw_data = list()
    for seq_idx, seq_type_1 in enumerate(sequence_types):
        col_data = data[data["Initial Label"] == seq_type_1][column].dropna()
        other_data = data[data["Initial Label"] != seq_type_1][column].dropna()
        try:
            
            #col_data = col_data[col_data > 0]
            #other_data = other_data[other_data > 0]
            FC = col_data.mean() / other_data.mean()

            if FC is None:
                FC = np.NAN
            MW_res = scipy.stats.mannwhitneyu(col_data, other_data, use_continuity=False, method="asymptotic")
            
            
            #curr_col_mw_data.append([column, seq_type_1, MW_res.statistic, MW_res.pvalue, log2FC])
            # if MW_res.pvalue < 0.05:
            #     pvalue = MW_res.pvalue
            #     if pvalue < ZERO_THRESHOLD:
            #         pvalue = 0
            #     MW_data.append([column, seq_type_1, seq_type_2, MW_res.statistic, pvalue])
        except (TypeError, ValueError):
            curr_col_mw_data.append([column, seq_type_1, np.NAN, np.NAN, FC])
        else:
            curr_col_mw_data.append([column, seq_type_1, MW_res.statistic, MW_res.pvalue, FC])
    # create df
    cur_col_MW_df = pd.DataFrame(curr_col_mw_data, columns=("Column", "Initial Label", "Mann-Whitney U statistic", "pvalue", "FC"))
    # rej, corrected_pvalues = statsmodels.stats.multitest.fdrcorrection(cur_col_MW_df["pvalue"])
    # cur_col_MW_df["corrected pvalue"] = corrected_pvalues
    # cur_col_MW_df = cur_col_MW_df[cur_col_MW_df["corrected pvalue"] < 0.05]
    MW_data.append(cur_col_MW_df)


MW_df = pd.concat(MW_data)
MW_df = MW_df[MW_df["pvalue"] < 0.05]
MW_df = MW_df.sort_values(by="pvalue", ascending=False)
#MW_df = pd.DataFrame(MW_data, columns=("Column", "Initial Label 1", "Initial Label 2", "Mann-Whitney U statistic", "pvalue"))
MW_df.to_csv("out_mannwhitney_fold_change.csv", sep=';', index=False)

MW_df["abs(FC)"] = MW_df["FC"].apply(np.abs)

gb = MW_df.sort_values(["pvalue", "abs(FC)"], ascending=[True, False]).groupby("Initial Label")
#gb.to_csv("out_mw_fold_change_sorted.csv", index=False)

with open("OUT_MW_FC_SORTED.txt", 'w') as f:
    for e in gb:
        f.write(e[0] + "\n\n")
        f.write(e[1].head(10)[["Column", "pvalue", "FC"]].to_string(index=False) + "\n\n")



OUTPUT_DIR = "boxplots"
# create output dir
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

data = pd.read_csv(INPUT_FILENAME, sep=',', low_memory=False)
sequence_types = list(data["Initial Label"].unique())

COLOR_PALETTE = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

for e in gb:
    errors = []
    initial_label = e[0]
    print(f"\t10 best for: {initial_label}")
    for pi, column in enumerate(e[1].head(10)["Column"]):
        

        if pi % 10 == 0:
            fig = plt.figure(1, figsize=(10.5, 16.5))
            plt.figure(1)
            
            plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.6)
        
        axes = plt.subplot(5, 2, pi % 10 + 1)
        #boxplot = data.boxplot(column=column, by="Initial Label", return_type='dict', patch_artist=True, ax=fig.gca(), grid=False, showfliers=False)
        boxplot = data.boxplot(column=column, by="Initial Label", return_type='dict', patch_artist=True, ax=axes, grid=False, showfliers=False)
        bp = boxplot[column]
        for patch, color in zip(bp['boxes'], COLOR_PALETTE):
            patch.set_facecolor(color)

        # fig.suptitle(column)
        axes.set_title(f"{pi+1}) {column}")
        seq_type = column.replace(" / ", "-")
        #column_file_name = str(column).replace("/", "slash").replace("|", "line")

        #plot_output_path = os.path.join(OUTPUT_DIR, f"{column_file_name}.png")
        if pi % 10 == 9 or pi == len(data_columns)-1:
            plt.suptitle(initial_label)
            plt.savefig(os.path.join(OUTPUT_DIR, f"grouped_boxplots_{initial_label}.png"))
            # plt.show()
            plt.close()
