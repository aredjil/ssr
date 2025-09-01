import numpy as np 
import matplotlib.pyplot as plt 
from pathlib import Path 

def main():
    root_path = Path(__file__).resolve().parent.parent.parent
    filename = root_path / "data" / "raw" / "zipf" / "ssr_1.txt"
    out_path = root_path / "results" / "figures" / "std" / "std_ssr.png"
    data = np.loadtxt(filename, dtype=int)


    unique, count = np.unique(data, return_counts=True)
    count = count / np.sum(count)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(unique, count, marker="s", color="tab:blue", label="Standard SSR")
    ax.set_xlabel("State")
    ax.set_ylabel("Frequency")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1E0, 1E4)
    ax.legend(frameon=True, edgecolor="black")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    plt.show()
    
    


if __name__ == "__main__":
    main()