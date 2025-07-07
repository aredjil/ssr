#! /usr/bin/env python3 

# script name: plot_average_avalanche_sizes.py
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import gamma

def main():
    x_lims = [1, 10E1, 10E3, 10E5]
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    ax = ax.flatten()

    for i, mu in enumerate([1.5, 2.0, 2.5, 3.0]):
        data = np.loadtxt(f"./data/raw/avalanche_sizes/results_{mu}.txt", dtype=int)

        counts, bin_edges = np.histogram(data, bins=34, density=False)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_width = bin_edges[1] - bin_edges[0]
        # Plot empirical counts as hollow circles
        
        # Fit Gamma distribution with floc=0
        shape, loc, scale = gamma.fit(data, floc=0)

        # Gamma PDF scaled to counts scale
        x = np.linspace(min(data), max(data), 100)
        pdf = gamma.pdf(x, shape, loc=loc, scale=scale)
        scaled_pdf = pdf * len(data) * bin_width
        ax[i].plot(bin_centers, counts, linestyle='None',
                marker='o',markerfacecolor='none', markersize=15, markeredgecolor='black', label='Simulation')
        # Plot scaled Gamma fit
        ax[i].plot(x, scaled_pdf, 'r--', linewidth=2, label=r'Fit to $\Gamma$ dist')

        ax[i].set_xlabel('Avalanche Size $s$')
        ax[i].set_ylabel('Frequency')
        ax[i].set_title(r'Avalanche Sizes ($\mu$={0}, N=$10^4$)'.format(mu))
        ax[i].set_xscale("log")
        ax[i].set_yscale("log")
        ax[i].set_xlim(x_lims[i], )
        ax[i].set_ylim(1, 10E2)
        ax[i].legend(loc="best")
        # plt.grid(True)
    fig.suptitle("Avalanche size distribution")
    plt.tight_layout()
    plt.savefig(f"./figures/avalanche_sizes_{mu}.png")
    plt.show()
if __name__ == "__main__":
    main()