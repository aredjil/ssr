#!/usr/bin/env python3

# script name: plot_average_avalanche_sizes.py
# NOTE: Fix the paths in all the python scripts 
# NOTE: Consider putting everything in one script 
import numpy as np 
import matplotlib.pyplot as plt 
import os 
import sys 


import yaml
import argparse 

from scipy.optimize import curve_fit
from matplotlib.ticker import NullFormatter, FixedLocator

"""
The aim of this code is to use the data store in ./data/figure3/
to reproduce the the distrubution of the cascade size in figure 3 in the below paper  
https://www.nature.com/articles/s41598-017-09836-4#auth-Stefan-Thurner-Aff1-Aff2-Aff3-Aff4 

"""


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def plot_fig(cfg):
    # Default configuration 
    plot_defaults = {
    "plot":{"input": "./data/raw/figure3/input", # Dir that stores the avalanche sizes per N and diff mu values  
    "Ns": [200, 400, 600, 800],  # Number of states used in generating the observations
    "markers": ["o", "s", ".", "^"], # Mathcing markers with the original paper  
    "colors": ["blue", "green", "black", "blue"], # Matching colors with the original paper 
    "special_facecolor_index": 2, 
    "x_label": r"Multiplicative parameter $\mu$", 
    "y_label": r"Average size $<s>$",
    "x_scale": "log",
    "y_scale": "log",
    "figsize": [5, 5],
    "save": True,
    "show": True,
    "output": "./results/figures/figure3/average_size.png" # Output file relative path 
    }
    } 
    # If the configuration file is not provided resort to the default settings   
    if cfg == None:
        cfg = plot_defaults
    # Getting the variables from the configuration file 
    input, Ns, markers, colors, special_idx, x_label, y_label, scale, y_scale, figsize, output_path = map(lambda k: cfg["plot"].get(k),
                                                                  ["input",
                                                                    "Ns", 
                                                                   "markers", 
                                                                   "colors", 
                                                                   "special_facecolor_index", 
                                                                   "x_label",
                                                                   "y_label",
                                                                   "x_scale",
                                                                   "y_scale",
                                                                   "figsize", 
                                                                   "output"])
    save, show = map(lambda k: cfg["plot"].get(k), ["save", "show"])

    plt.figure(figsize=figsize)
    for i, n in enumerate(Ns):
        mus = np.linspace(1.5, 3.5, 20).round(decimals=1)
        xticks = [10**0.2, 10**0.5]
        xtick_labels = [r'$10^{0.2}$', r'$10^{0.5}$']
        label = "Fit" if i == 0 else None
        facecolor = "none" if i != special_idx else "black"

        cascade_sizes = []
        for mu in mus:
            data = np.loadtxt(f"{input}_{n}_{mu}.txt", dtype=float)
            cascade_sizes.append(data.mean())
        
        
        plt.scatter(mus, cascade_sizes, label=r"$N$={0}".format(n), marker=markers[i], facecolors=facecolor, edgecolors=colors[i])

        plt.xscale(scale)
        plt.yscale(scale)

        plt.xticks(xticks, xtick_labels)
        ax = plt.gca()  
        ax.xaxis.set_minor_locator(FixedLocator([]))
        ax.xaxis.set_minor_formatter(NullFormatter())
        plt.ylabel(r"{0}".format(y_label))
        plt.xlabel(r"{0}".format(x_label))
        plt.ylim(10E0, )
        plt.xlim(mus[0], mus[-1])
        plt.legend(loc="best", title="Number of states", edgecolor="black", frameon=True)
    plt.tight_layout()
    # Save the figure 
    if save:
        plt.savefig(output_path)
        print(f"Figure saved at: {output_path}")
    # Show the figure
    if show:
        plt.show()
    plt.close()

def main(cfg):
    plot_fig(cfg)

if __name__ == "__main__":
    # Parse the arguements from the user 
    parser = argparse.ArgumentParser(description="placeholder text...")
    parser.add_argument("--config", required=False, help="Path to YAML config")
    args = parser.parse_args()

    config = load_config(args.config) if args.config else None 
    main(config)