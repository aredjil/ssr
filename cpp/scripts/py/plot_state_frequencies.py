#! /usr/bin/env python3 

# This script fits the data and save the result to a text file in the working directory 
import numpy as np 
import powerlaw 
import contextlib
import sys
import os
import matplotlib.pyplot as plt 
import h5py
"""
This python script reproduces the figure 1 from the paper based on the data input_mu.txt
"""

def main():
    obs_dir = "./data/processed/hdf5/data_"
    markers = [
                "s",
                "*", 
                "*", 
                "o", 
                "^", 
    ]
    colors = ["darkblue", 
              "blue", 
              "green", 
              "black", 
              "red", 
              ]
    
    fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

    for i, mu in enumerate([0.5, 
                            1.0, 
                            1.5, 
                            2.0, 
                            2.5, 
                            # 3.0
                            ]
                            ):
        filename = f"{obs_dir}{mu}.h5"
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            # pass 
        else:
            with h5py.File(filename, "r") as f:
                unique = f["unique"][:]
                unique_count = f["count"][:]

            frequency = unique_count / np.sum(unique_count)

            axis.plot(unique, frequency, label=r" $\mu$={0}".format(mu), marker=markers[i], markerfacecolor='none', markersize=8, linestyle="None", color=colors[i])
            axis.legend(frameon=True, edgecolor="black", title="Multiplicative Factor")
            axis.set_xscale('log')
            axis.set_yscale('log')
            axis.set_xlabel("State")
            axis.set_ylabel("Relative Frequency")
            axis.set_xlim(1E0, 1E4)
            axis.set_ylim(1E-7, 1E-1)

    # fig.suptitle("Frequency of Visits Per State")
    plt.tight_layout()
    plt.savefig("./figures/figure1/state_visits_relative_frequency.png")
    plt.show()

if __name__== "__main__":
    main()


