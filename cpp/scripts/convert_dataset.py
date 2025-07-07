import numpy as np
import h5py
import matplotlib.pyplot as plt
from collections import Counter
"""
 This script converts the data from .txt files to .h5 files 
 This dramatically decreases the size of the files 
 and allow plotting the state visits histogram (figure 1)
 
"""
def main():
    for mu in [0.5]:
        filename = f"./data/figure1/input_{mu}.txt"
        counter = Counter()
        
        # Read and count in chunks
        with open(filename, "r") as f:
            for line in f:
                try:
                    val = float(line.strip())
                    counter[val] += 1
                except ValueError:
                    continue  # skip bad lines
        
        # Convert to arrays
        unique = np.array(list(counter.keys()))
        count = np.array(list(counter.values()))
        
        # Save to HDF5
        with h5py.File(f"data_{mu}.h5", "w") as f:
            f.create_dataset("unique", data=unique, compression="gzip")
            f.create_dataset("count", data=count, compression="gzip")
        
if __name__ == "__main__":
    main()