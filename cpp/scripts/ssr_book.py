#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from nltk.tokenize import word_tokenize
from collections import Counter
import powerlaw
import nltk
# nltk.download('punkt')

def count_words_nltk(filename: str):
    """Counts word frequencies using NLTK tokenizer, filtering out punctuation."""
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
        words = word_tokenize(text)
        words = [word for word in words if word.isalpha()]
        return Counter(words)

def main():
    root = Path(__file__).resolve().parent.parent
    book_path = root / "data" / "books" / "Moby-Dick.txt"
    ssr_path = root / "mob.txt"
    out_figure = root / "results" / "figures" / "moby_word_ssr.png"

    # Load SSR data
    ssr_data = np.loadtxt(ssr_path)
    ssr_data = np.array(sorted(Counter(ssr_data).values(), reverse=True))
    ssr_data = ssr_data /np.sum(ssr_data)

    ssr_ranks = np.arange(1, len(ssr_data)+1)

    # Count words
    word_counts = count_words_nltk(book_path)

    freqs = np.array(sorted(word_counts.values(), reverse=True))
    freqs = freqs /np.sum(freqs)
    ranks = np.arange(1, len(freqs)+1)

    # Fit power-law to word ranks
    # repeated_ranks = np.repeat(ranks, freqs)
    # fit = powerlaw.Fit(repeated_ranks, discrete=True, verbose=False)
    # alpha = fit.alpha
    # xmin = fit.xmin

    # mask = ranks >= int(xmin)
    # pdf_probs = fit.power_law.pdf(ranks[mask])
    # pdf_counts = pdf_probs * len(repeated_ranks)

    # Plot
    plt.figure(figsize=(8,6))
    plt.loglog(ranks, freqs, marker='o', linestyle='none', mfc='none', alpha=0.6, label="Word Frequency")
    # plt.loglog(ranks[mask], pdf_counts, linestyle="--", color="black", label=f"Power-law fit (α={alpha:.2f})")
    # plt.axvline(x=xmin, color="red", ls="--", alpha=0.5, label=r"$x_{\mathrm{min}}$")

    plt.loglog(ssr_ranks, ssr_data, marker='x', linestyle='none', color='red', alpha=0.7, label="SSR")

    plt.xlabel("Rank/State")
    plt.ylabel("Frequency")
    plt.title(f"Moby-Dick Word & SSR State Frequencies")
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.legend()
    
    out_figure.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_figure)
    plt.show()
    print(f"Figure saved to: {out_figure}")

if __name__ == "__main__":
    main()
