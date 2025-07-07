import numpy as np 
import matplotlib.pyplot as plt 
import powerlaw
# function to plot the noisy ssr data based on the noise strngth 
def plot_data(filename, file_range, ax, colors):
    for i, lam in enumerate(file_range):
        data = np.loadtxt(filename + str(lam) + ".txt", dtype=int)
        unique, count = np.unique(data, return_counts=True)
        ax.scatter(unique, count, label=fr"$\lambda$={lam}", s=10, c=colors[i])
        ax.legend(loc="best", title=fr"Noise Strength $\lambda$", shadow=True, frameon=True, edgecolor="black")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("States")
        ax.set_xlabel("Number of Visits")
        ax.set_xlim(unique[0], unique[-1])
    return ax 



filename = "./data/raw/noisy_ssr/output_"
file_range = [0.5, 0.7, 1.0]
colors = ["blue", "red", "black"]
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(5, 5))
plot_data(filename, file_range, ax, colors)    
plt.savefig("./figures/noisy_ssr/noisy_ssr.png")                                                                                                                                                                                                                                                                                                                                                                  
plt.show()

# data = np.loadtxt("./output_0.5.txt", dtype=int)
# data1 = np.loadtxt("./output_0.7.txt", dtype=int)
# data2 = np.loadtxt("./output_1.0.txt", dtype=int)

# unique, count = np.unique(data, return_counts=True)
# unique1, count1 = np.unique(data1, return_counts=True)
# unique2, count2 = np.unique(data2, return_counts=True)


# # fit = powerlaw.Fit(data, verbose=False, discrete=True)
# # print(f"Alpha: {fit.alpha}")
# # print(f"xmin: {fit.xmin}")
# # print(f"Alpha: {fit.alpha}")
# plt.scatter(unique2, count2, label=f"1.0")

# plt.scatter(unique, count, label=f"0.5")
# plt.scatter(unique1, count1, label=f"0.7")
# plt.xlim(unique[0], unique[-1])
# plt.xscale("log")
# plt.yscale("log")
# plt.legend(loc="best", shadow=True)
# plt.xlabel("States")
# plt.ylabel("Frequency")
# plt.savefig("./noisy_ssr.png")
# plt.show()