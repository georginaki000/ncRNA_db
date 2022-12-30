import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "boxplots"
INPUT_FILENAME = "OUT_ALL_CLEAN.csv"

# create output dir
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

data = pd.read_csv(INPUT_FILENAME, sep=',', low_memory=False)
sequence_types = list(data["Initial Label"].unique())

print(sequence_types)

trfs = data[data["Initial Label"] == "trf"]

data_columns = data.columns.values[10:]

COLOR_PALETTE = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

errors = []
for pi, column in enumerate(data_columns):
    print(f"\tColumn: {column}")

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
    axes.set_title(column)
    seq_type = column.replace(" / ", "-")
    #column_file_name = str(column).replace("/", "slash").replace("|", "line")

    #plot_output_path = os.path.join(OUTPUT_DIR, f"{column_file_name}.png")
    if pi % 10 == 9 or pi == len(data_columns)-1:
        plt.savefig(os.path.join(OUTPUT_DIR, f"grid_boxplots_{pi // 10 + 1}.png"))
        # plt.show()
        plt.close()
    