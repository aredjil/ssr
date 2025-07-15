#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
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
    root_path = Path(__file__).resolve().parent.parent
    dir_path = root_path / "data" / "books"
    out_figure = root_path / "results" / "figures" / "words_count_in_books.png"
    out_data_dir = root_path / "data" / "raw" / "rank_counts"

    # List of book files
    books = [
        "Moby-Dick.txt", 
        "Oliver-Twist.txt"
    ]
    filenames = [dir_path / book for book in books]

    plt.figure(figsize=(6, 6))

    for filename in filenames:
        word_counts = count_words_nltk(filename)
        freqs = np.array(sorted(word_counts.values(), reverse=True))
        ranks = np.arange(1, len(freqs) + 1)

        # Save repeated ranks to file
        repeated_ranks = np.repeat(ranks, freqs)
        obs_file = out_data_dir / filename.name.replace('.txt', '.dat')
        obs_file.parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(obs_file, repeated_ranks, fmt="%d")

        # Plot
        label = filename.name.replace('-', ' ').removesuffix(".txt") + f" [n={len(ranks)}]"
        plt.loglog(ranks, freqs, marker='o', linestyle='none', mfc='none', markersize=4, alpha=0.6, label=label)

    # Finalize plot
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.xlim(1E0, 1E4)
    plt.ylim(1E0, )
    plt.legend(frameon=True, edgecolor="black", shadow=True, title="Book", title_fontsize="large")
    plt.tight_layout()

    # Save figure
    out_figure.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_figure)
    plt.show()
    print(f"Figure saved to: {out_figure}")

if __name__ == "__main__":
    main()
