#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
from pathlib import Path

def main():
    # Root path of the project
    root_path = Path(__file__).resolve().parent.parent.parent

    # Plotting configuration
    Ns = [200, 400, 600, 800]
    markers = ["o", "s", ".", "^"]
    colors = ["blue", "green", "black", "blue"]
    special_idx = 2  # Only this index has black facecolor
    figsize = (5, 5)
    xticks = [10**0.2, 10**0.5]
    xtick_labels = [r'$10^{0.2}$', r'$10^{0.5}$']
    x_label = r"Multiplicative parameter $\mu$"
    y_label = r"Average size $<s>$"

    # Input/output
    input_prefix = root_path / "data" / "raw" / "figure3" / "input"
    out_path = root_path / "results" / "figures" / "figure3" / "average_size.png"
    # Create output directory if it doesn't exist
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Start plotting
    plt.figure(figsize=figsize)
    for i, N in enumerate(Ns):
        mus = np.linspace(1.5, 3.5, 20).round(1)
        cascade_sizes = []

        for mu in mus:
            file_path = input_prefix.parent / f"{input_prefix.name}_{N}_{mu}.txt"
            data = np.loadtxt(file_path, dtype=float)
            cascade_sizes.append(data.mean())

        # Scatter points
        facecolor = "black" if i == special_idx else "none"
        plt.scatter(mus, cascade_sizes,
                    label=f"N={N}",
                    marker=markers[i],
                    facecolors=facecolor,
                    edgecolors=colors[i])
        
        # Dotted connecting line
        plt.plot(mus, cascade_sizes, ls="--", c="tab:red", alpha=0.5)

    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(xticks, xtick_labels)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(mus[0], mus[-1])
    plt.ylim(1e1, 1e5)  # adjust if needed

    ax = plt.gca()
    ax.xaxis.set_minor_locator(FixedLocator([]))
    ax.xaxis.set_minor_formatter(NullFormatter())

    plt.legend(loc="best", title="Number of states", edgecolor="black", frameon=True)
    plt.tight_layout()

    # Save and show
    plt.savefig(out_path)
    print(f"Figure saved at: {out_path}")
    plt.show()

if __name__ == "__main__":
    main()
