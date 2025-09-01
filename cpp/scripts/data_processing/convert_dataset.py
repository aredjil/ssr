import numpy as np
import h5py
from pathlib import Path

"""
This script converts the data from .txt files to .h5 files.
It saves the raw array of values instead of unique counts.
"""

def main():
    root_path = Path("./")
    print(f"Root path: {root_path}")

    for mu in [0.5, 1.0, 1.5, 2.0, 2.5]:
        filename = root_path / "data" /"raw"/"figure1" / f"input_{mu}.txt"

        # Read values into a list
        values = []
        with open(filename, "r") as f:
            for line in f:
                try:
                    val = float(line.strip())
                    values.append(val)
                except ValueError:
                    continue  # skip bad lines

        # Convert list to NumPy array
        values_array = np.array(values)

        # Save the raw array to HDF5
        h5_filename = f"./data_{mu}.h5"
        with h5py.File(h5_filename, "w") as f:
            f.create_dataset("values", data=values_array, compression="gzip")
        
        print(f"Saved {len(values_array)} values to {h5_filename}")

if __name__ == "__main__":
    main()
