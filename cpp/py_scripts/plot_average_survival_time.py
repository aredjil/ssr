#!/usr/bin/env python3 

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import NullFormatter, FixedLocator


def main():
    # Iterate over the data files that contain the observations 
    # per size and per mu 
    markers = [
        "^", 
        "o", 
        "*", 
        "s"

    ]
    colors = [
        "blue", 
        "red", 
        "green", 
        "black"
    ] 
    plt.figure(figsize=(5, 5))
    xticks = [10**0.2, 10**0.5]
    xtick_labels = [r'$10^{0.2}$', r'$10^{0.5}$']
    for i, N in enumerate(np.arange(200, 1000, 200)):
        y = []
        mus = np.arange(1.5, 3.1, 0.1)
        for mu in mus:
            mu = round(mu, 3)
            data = np.loadtxt(f"./data/durations/data_{N}_{mu}.txt", dtype=int)
            y.append(data.mean())
        plt.plot(mus, y, linestyle="None", marker=markers[i],markerfacecolor='none', markersize=8, markeredgecolor=colors[i],
                label=f"N={N}")
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(xticks, xtick_labels)
    ax = plt.gca()  
    ax.xaxis.set_minor_locator(FixedLocator([]))
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.xlabel(r"Multiplicative Factor $\mu$")
    plt.xlim(mus[0], )
    plt.ylabel(f"Average cascade Survival Time <$\Delta$ t>")
    plt.legend(loc="best", shadow=True)
    plt.tight_layout()
    plt.savefig("./figures/durations/average_duration.png")
    plt.show()
if __name__ == "__main__":
    main()



