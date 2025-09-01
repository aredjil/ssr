#!/usr/bin/env python3 

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import gamma
from matplotlib.ticker import FuncFormatter, LogLocator
import sys 
from pathlib import Path 
 
def main():
    root_path = Path(__file__).resolve().parent.parent.parent
    out_path = root_path / "results" / "durations"
    for i, mu in enumerate([1.0, 1.5, 2.0, 2.5]):
        filename = root_path / "data" / "raw" / "durations" / f"data_{mu}.txt"
        data = np.loadtxt(filename, dtype=int)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
        # Load the data 
        # Get the counts and bin_edges 
        counts, bin_edges = np.histogram(data, bins=30, density=False)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_width = bin_edges[1] - bin_edges[0]
        #Fit the data to gamma distrubution     
        shape, loc, scale = gamma.fit(data, floc=0)

        # Gamma PDF scaled to counts scale
        x = np.linspace(min(data), max(data), 100)
        pdf = gamma.pdf(x, shape, loc=loc, scale=scale)
        scaled_pdf = pdf * len(data) * bin_width
        ax.plot(bin_centers, counts, linestyle='None',
                marker='o',markerfacecolor='none', markersize=15, markeredgecolor='black', label='Simulation')
        # Plot scaled Gamma fit
        ax.plot(x, scaled_pdf, 'r--', linewidth=2, label=r'Fit to $\Gamma$ dist')


        ax.set_xlabel(r'Cascade Survival Time $\tau$')
        ax.set_ylabel('Frequency')
        ax.set_title(r'Cascade Survival Time distribution($\mu$={0}, N=$10^4$)'.format(mu))
        plt.xscale("log")
        plt.yscale("log")
        plt.xlim(1, )
        plt.ylim(0, )
        ax.legend(loc="best")
        plt.tight_layout()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path/ f"duration_dist_{mu}.png")
        plt.show()
if __name__ == "__main__":
    main()
