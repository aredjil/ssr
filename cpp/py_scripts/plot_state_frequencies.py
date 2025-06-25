#! /usr/bin/env python3 

# This script fits the data and save the result to a text file in the working directory 
import numpy as np 
import powerlaw 
import contextlib
import sys
import os
import matplotlib.pyplot as plt 
"""
This python script reproduces the figure 1 from the paper based on the data input_mu.txt
NOTE: Make the paths absolute
"""



@contextlib.contextmanager
def suppress_stdout():
    """
    A function to disbale the output of the function powerlaw.Power_Law().generate_ramdom()...
    """
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
def main():
    obs_dir = "./data/figure1/input_"
    markers = [
                "s",
                "*", 
                "*", 
                "o", 
                "^", 
                # ">"
    ]
    colors = ["darkblue", 
              "blue", 
              "green", 
              "black", 
              "red", 
            #   "purple"
              ]
    
    fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
    # axis = axis.flatten()

    for i, mu in enumerate([0.5, 
                            1.0, 
                            1.5, 
                            2.0, 
                            2.5, 
                            # 3.0
                            ]
                            ):
        filename = f"{obs_dir}{mu}.txt"
        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            # pass 
        else:
            data = np.loadtxt(filename, dtype=int)
            unique, unique_count = np.unique(data, return_counts=True)
            
            frequency = unique_count / np.sum(unique_count)

            axis.plot(unique, frequency, label=r" $\mu$={0}".format(mu), marker=markers[i], markerfacecolor='none', markersize=8, linestyle="None", color=colors[i])
            axis.legend()
            axis.set_xscale('log')
            axis.set_yscale('log')
            axis.set_xlabel("State")
            axis.set_ylabel("Relative Frequency")
            axis.set_xlim(1, 10E3)
            axis.set_ylim(10E-8, 10E-2)

    # fig.suptitle("Frequency of Visits Per State")
    plt.tight_layout()
    plt.savefig("./figures/figure1/state_visits_relative_frequency.png")
    plt.show()

if __name__== "__main__":
    main()


