import pandas as pd
import matplotlib.pyplot as plt
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

data_columns = data.columns.values[2:]

COLOR_PALETTE = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

kruskal_data = []
MW_data = []
KS_data = []
# Kruskal wallis
ZERO_THRESHOLD = 1e-5
for column in data_columns:
    kwdata = []
    for seq_idx, seq_type in enumerate(sequence_types, start=1):
        active_data =  data[data["Initial Label"] == seq_type][column].dropna()
        kwdata.append(active_data)
    # https://stackoverflow.com/questions/51632900/pandas-apply-kruskal-wallis-to-numeric-columns
    kruskal = scipy.stats.kruskal(*kwdata, nan_policy="omit")
    kruskal_data.append([column, *kruskal])


    curr_col_mw_data = []
    for seq_idx, seq_type_1 in enumerate(sequence_types[:-1]):
        for seq_type_2 in sequence_types[seq_idx+1:]:
            seq1_data = data[data["Initial Label"] == seq_type_1][column].dropna()
            seq2_data = data[data["Initial Label"] == seq_type_2][column].dropna()
            try:
                MW_res = scipy.stats.mannwhitneyu(seq1_data, seq2_data, use_continuity=False, method="asymptotic")
                curr_col_mw_data.append([column, seq_type_1, seq_type_2, MW_res.statistic, MW_res.pvalue])
                # if MW_res.pvalue < 0.05:
                #     pvalue = MW_res.pvalue
                #     if pvalue < ZERO_THRESHOLD:
                #         pvalue = 0
                #     MW_data.append([column, seq_type_1, seq_type_2, MW_res.statistic, pvalue])
            except (TypeError, ValueError):
                pass
            
            try:
                KS_res = scipy.stats.kstest(seq1_data, seq2_data)
                KS_data.append([column, seq_type_1, seq_type_2, KS_res.statistic, KS_res.pvalue])
            except (TypeError, ValueError):
                pass
    # create df
    cur_col_MW_df = pd.DataFrame(curr_col_mw_data, columns=("Column", "Initial Label 1", "Initial Label 2", "Mann-Whitney U statistic", "pvalue"))
    rej, corrected_pvalues = statsmodels.stats.multitest.fdrcorrection(cur_col_MW_df["pvalue"])
    cur_col_MW_df["corrected pvalue"] = corrected_pvalues
    cur_col_MW_df = cur_col_MW_df[cur_col_MW_df["corrected pvalue"] < 0.05]
    MW_data.append(cur_col_MW_df)


ks_df = pd.DataFrame(KS_data, columns=("Column", "Initial Label 1", "Initial Label 2", "KS statistic", "pvalue"))
# ks_df[ks_df["pvalue"] < ZERO_THRESHOLD]["pvalue"] = 0.0
ks_df = ks_df[ks_df["pvalue"] < 0.05]
ks_df = ks_df.sort_values(by="pvalue", ascending=False)
ks_df.to_csv("out_KS.csv", sep=';', index=False)

kruskal_df = pd.DataFrame(kruskal_data, columns=("Column", "H statistic", "pvalue"))
kruskal_df = kruskal_df[kruskal_df["pvalue"] < 0.05]
kruskal_df = kruskal_df.sort_values(by="pvalue", ascending=False)
kruskal_df.to_csv("out_kruskal.csv", sep=';', index=False)

MW_df = pd.concat(MW_data)
MW_df = MW_df[MW_df["pvalue"] < 0.05]
MW_df = MW_df.sort_values(by="pvalue", ascending=False)
#MW_df = pd.DataFrame(MW_data, columns=("Column", "Initial Label 1", "Initial Label 2", "Mann-Whitney U statistic", "pvalue"))
MW_df.to_csv("out_mannwhitney.csv", sep=';', index=False)

errors = []
for column in data_columns:
    print(f"\tColumn: {column}")
    
    
    try:
        plt.figure(figsize=(18.5, 10.5))
        ax_share = None

        n_bins = 20

        sep_data = []

        for seq_idx, seq_type in enumerate(sequence_types, start=1):
            active_data =  data[data["Initial Label"] == seq_type]
            print(f"Running: {seq_type}")
            
            clr = COLOR_PALETTE[seq_idx-1]

            if ax_share:
                plt.subplot(len(sequence_types), 1, seq_idx, sharex=ax_share, sharey=ax_share)
            else:
                ax_share = plt.subplot(len(sequence_types), 1, seq_idx)

            

            if len(active_data[column].unique()) <= DISTINCT_THRESHOLD:
                val_counts = dict(active_data[column].value_counts())
                bar_labels = sorted(list(map(str, val_counts.keys())))
                plt.bar(bar_labels, [x / len(active_data[column]) for x in val_counts.values()], color=clr, alpha=0.7, label=seq_type)
            
            else:

                # n_bins = 0
                # try:
                #     n_bins = math.ceil((active_data[column].max() - active_data[column].min()) / 0.5)
                # except TypeError:
                #     print("\t\tNo numeric data!")
                #     continue
                
                # except OverflowError:
                #     print("\t\tInf values!")
                #     continue
                
                # finally:
                #     plt.close()
                
                h, _, _ = plt.hist(active_data[column], n_bins, facecolor=clr, alpha=0.7, density=True, label=seq_type)
                sep_data.append(h)

            plt.grid(True)
            plt.xlabel(column)
            plt.ylabel('Density')
            # fig.yscale('log')
            #plt.title(f"Column: {column}")
            # plt.show()
            plt.plot([], [], ' ', label=f"mean: {active_data[column].mean()}")
            plt.plot([], [], ' ', label=f"stdev: {active_data[column].std()}")
            plt.legend()
        


        plt.suptitle(f"Column: {column}")
        seq_type = seq_type.replace(" / ", "-")
        column_file_name = str(column).replace("/", "slash").replace("|", "line")

        plot_output_path = os.path.join(OUTPUT_DIR, f"{column_file_name}.png")
        plt.savefig(plot_output_path)
        #plt.show()
        plt.close()
    
    except (TypeError, ValueError) as e:
        print(f"Could not plot Column: {column}")
        errors.append([column, str(e)])


print("Errors: ", errors)
# kruskal_df = pd.DataFrame(kruskal_data, columns=("Initial Label", "H statistic", "pvalue"))
# kruskal_df.to_csv("out_kruskal.csv", sep=';', index=False)