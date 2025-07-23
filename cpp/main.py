import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


path = "./data"

mus = [0.5, 1.0, 1.5]

plt.figure()
for mu in mus:
    data = np.loadtxt(path + f"_{mu}.txt", dtype=int)
    count = Counter(data)
    count = count.most_common()
    unique = list(key for key, _ in count)
    counts = list(values for _, values in count)
    plt.scatter(unique, counts)
    plt.xscale("log")
    plt.yscale("log")
plt.show()