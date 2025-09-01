import numpy as np 
import matplotlib.pyplot as plt 
from collections import Counter 
import powerlaw 
from scipy.optimize import curve_fit


def power_law(x, a, b):
    return a * x**b
# data = np.loadtxt("./data/raw/zipf/ssr_1.0.txt", dtype=int)
# Load the data for the different values of lambda 
colors = [
    'tab:blue', 
    'tab:green', 
    'lightblue'
]
i = 0 
plt.plot()
for noise in [0.5, 0.7, 1.0]:
    data = np.loadtxt(f"./data/raw/noisy_ssr/output_{noise}.txt", dtype=int)
    # data = data[:10_000]

    count = Counter(data)

    most_common = count.most_common()
    ranks = np.array([item[0] for item in most_common])
    counts = np.array([item[1] for item in most_common])


    # CUrvefit 
    # popt, pcov = curve_fit(power_law, ranks, counts, p0=(1, 1))  # p0 = initial guess
    # a, b = popt

    # print(f"Fit: y = {a:.3f} * x^{b:.3f}")
    # counts = counts / np.sum(counts)

    # fit = powerlaw.Fit(data=data, discrete=True, verbose=False)

    # mask = ranks >= int(fit.xmin)           
    # pdf_probs = fit.power_law.pdf(ranks[mask])   
    # pdf_counts = pdf_probs * len(data)         


    # print(f"Alpha: {fit.alpha}")
    # print(f"xmin: {fit.xmin}")
    # print(f"D: {fit.D}")

    plt.loglog(ranks, counts, color=colors[i], marker='o', linestyle='none', mfc='none', markersize=4, alpha=0.8, label=rf'Empirical,  $\lambda$ = {abs(noise):.2}')
    # Plot the result of curve_fit 
    # plt.loglog(ranks, powe            r_law(ranks, a, b), marker='none', linestyle='--', mfc='none', label=fr'Fit, $\lambda$ = {abs(b):.2}')
    i+=1
    # plt.loglog(ranks[mask], pdf_counts, linestyle="--", color="tab:red", label=rf'Fit [$\hat{{\alpha}}$: {fit.alpha:.3f}]')
plt.xlabel("States")
plt.ylabel("Frequency")
plt.xlim(1E0, 1E4)
plt.legend(loc="best", edgecolor="black")
plt.savefig("./results/figures/noisy_fit.png")
plt.show()