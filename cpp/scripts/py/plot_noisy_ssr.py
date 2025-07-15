import numpy as np 
import matplotlib.pyplot as plt 
from pathlib import Path 

# function to plot the noisy ssr data based on the noise strngth 
def plot_data(filename, file_range, ax, colors):
    for i, lam in enumerate(file_range):
        data = np.loadtxt(filename + str(lam) + ".txt", dtype=int)
        unique, count = np.unique(data, return_counts=True)
        ax.scatter(unique, count, label=fr"$\lambda$={lam}", s=10, c=colors[i])
        ax.legend(loc="best", title=fr"Noise Strength $\lambda$", shadow=True, frameon=True, edgecolor="black")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("States")
        ax.set_xlabel("Number of Visits")
        ax.set_xlim(unique[0], unique[-1])
    return ax 

def main():
    root_path = Path(__file__).resolve().parent.parent.parent
    in_filename = root_path / "data" / "raw" / "noisy_ssr" / "output_"
    out_filename = root_path / "figures" / "noisy_ssr" / "noisy_ssr.png"
    file_range = [0.5, 0.7, 1.0]
    colors = ["blue", "red", "black"]
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(5, 5))
    plot_data(in_filename, file_range, ax, colors)    
    out_filename.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_filename)                                                                                                                                                                                                                                                                                                                                                                  
    plt.show()
if __name__ == "__main__":
    main()