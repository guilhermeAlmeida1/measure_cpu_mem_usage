import pandas as pd
import argparse
import pathlib
import matplotlib.pyplot as plt
import psutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CPU and memory consumption of binary program.")

    parser.add_argument("inputs", nargs="+", type=pathlib.Path, help="Input data")

    parser.add_argument("-o", "--output_dir", type=pathlib.Path, help="Output Directory")

    args = parser.parse_args()

    inputs = args.inputs

    dfs = []
    for input in inputs:
        try:
            with open(input, "r") as f:
                df = pd.read_csv(f, delimiter=' ')

                df["time"] = df["time"] - df["time"][0]
                dfs.append(df)

    ##################################
    # Plot all metrics each dataset. #
    ##################################

                fig, ax = plt.subplots()
                ax2 = ax.twinx()
                ax.set_ylabel("%")
                ax2.set_ylabel("bytes")
                ax.plot(df["time"], df[r"%cpu"], label=r"CPU usage (%)",    marker='', markersize=5, linestyle="-", linewidth=1, color="r")
                ax.plot(df["time"], df[r"%mem"], label=r"Memory usage (%)", marker='', markersize=5, linestyle="-", linewidth=1, color="g")
                ax2.plot(df["time"], df["mem_used"], label="mem_used",      marker='', markersize=5, linestyle="-", linewidth=1, color="b")
                ax2.plot(df["time"], df["mem_active"], label="mem_active",  marker='', markersize=5, linestyle="-", linewidth=1, color="y")
                fig.legend(loc="upper left", fontsize=8)
                plt.savefig(args.output_dir.joinpath(str(input.stem) + ".pdf"))
                plt.close()
        except:
            print("Error reading input file " + str(input))

    ###############################################
    # Plot each metric for all datasets together. #
    ###############################################
    datasets = [r"%cpu", r"%mem", "mem_used", "mem_active"]
    labels = [r"CPU usage (%)", r"Memory usage (%)", "Memory usage (byte)", "mem_active"]
    colors = ["r", "g", "b", "y"]
    for i in range(0,len(datasets)):
        dataset = datasets[i]
        for j in range(0,len(dfs)):
            df = dfs[j]
            plt.plot(df["time"], df[dataset], label=str(inputs[j].stem), marker ='', linestyle='-', linewidth=1, color = colors[j % len(colors)])
        plt.legend(loc="upper left", fontsize=8)
        plt.xlabel("Time")
        plt.ylabel(labels[i])
        plt.savefig(args.output_dir.joinpath(labels[i] + ".pdf"))
        plt.close()
