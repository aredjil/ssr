#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import powerlaw
import nltk

nltk.download('punkt')

def count_words_nltk(filename: str):
    """
    Counts word frequencies using NLTK tokenizer, filtering out punctuation.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
        words = word_tokenize(text)
        words = [word for word in words if word.isalpha()]
        return Counter(words)

def main():
    # Define root paths
    root_path = Path(__file__).resolve().parent.parent.parent
    dir_path = root_path / "data" / "books"
    out_figure = root_path / "results" / "figures" / "words_count_in_books.png"
    out_data_dir = root_path / "data" / "raw" / "rank_counts"

    # List of book files
    books = [
        "Moby-Dick.txt",
        "Oliver-Twist.txt",
        "Ulysses.txt"
    ]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    filenames = [dir_path / book for book in books]

    fig, ax = plt.subplots(ncols=1, nrows=3, figsize=(6, 9))
    ax = ax.flatten()
    for i, filename in enumerate(filenames):
        word_counts = count_words_nltk(filename)
        freqs = np.array(sorted(word_counts.values(), reverse=True))
        ranks = np.arange(1, len(freqs) + 1)

        # Save repeated ranks to file
        repeated_ranks = np.repeat(ranks, freqs)
        fit = powerlaw.Fit(repeated_ranks)
        alpha = fit.alpha 
        xmin = fit.xmin
        D = fit.D

        mask = ranks >= int(fit.xmin)           
        pdf_probs = fit.power_law.pdf(ranks[mask])   
        pdf_counts = pdf_probs * len(repeated_ranks)         

        # Plot
        label_alpha = rf'$\hat{{\alpha}} = {alpha:.3f}$'
        label_xmin = rf'$x_{{min}} = {int(xmin)}$'
        label_D = rf'$D = {D:.3f}$'
        label_fit = rf'powerlaw fit'

        label = filename.name.replace('-', ' ').removesuffix(".txt") + f" [n={len(ranks)}]"
        ax[i].loglog(ranks, freqs, color=colors[i], marker='o', linestyle='none', mfc='none', markersize=4, alpha=0.6, label=label)
        ax[i].loglog(ranks[mask], pdf_counts, linestyle="--", color="black", label=label_fit)
        ax[i].axvline(x=xmin, color="red", ls="--", label=label_xmin, alpha=0.5)
        # fit.power_law.plot_pdf(label="fit", ax=ax[i])
        ax[i].plot([], [], color=colors[i], marker='none', linestyle='none', mfc='none', markersize=4, alpha=0.6, label=label_alpha)
        ax[i].plot([], [], color=colors[i], marker='none', linestyle='none', mfc='none', markersize=4, alpha=0.6, label=label_D)
        ax[i].text(xmin, ax[i].get_ylim()[0], r"$x_{\mathrm{min}}$", 
           color="red", ha="center", va="bottom")
        # xticks = list(ax[i].get_xticks())       # current tick positions
        # xticks.append(xmin)                     # add xmin position
        # xticklabels = [rf"$x_{{min}}$" if t == xmin else str(int(t)) for t in xticks]
        # ax[i].set_xticks(xticks)
        # ax[i].set_xticklabels(xticklabels)
    # Finalize plot
        ax[i].set_xlabel("Rank")
        ax[i].set_ylabel("Frequency")
        ax[i].grid(True, which="both", ls="--", lw=0.5)
        ax[i].set_xlim(1E0, 1E4)
        ax[i].set_ylim(1E0, )
        ax[i].legend(frameon=True, edgecolor="black", shadow=True, title="Book Title", title_fontsize="large")

    plt.tight_layout()

    # Save figure
    out_figure.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_figure)
    plt.show()
    print(f"Figure saved to: {out_figure}")

if __name__ == "__main__":
    main()
