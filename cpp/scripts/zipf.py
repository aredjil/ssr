#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import powerlaw
import nltk
# nltk.download('punkt')

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
    # The current path of this file :) 
    root = Path(__file__).resolve().parent
    # Directory of the text files that contain the content of the books 
    dir_path = root / "data" / "books"
    # Ouput directory 
    out_figure = root / "results" / "figures" / "words_count_in_books.png"

    books = [
        "Strange-Case-of-Dr.-Jekyll-and-Mr.-Hyde.txt",
        "The-Call-of-the-Wild.txt",
        "The-Metamorphosis.txt",
        "A-Christmas-Carol.txt",
        "The-War-of-the-Worlds.txt",
        "The-Adventures-of-Tom-Sawyer.txt",
        "Treasure-Island.txt",
        "The-Time-Machine.txt",
        "Frankenstein.txt",
        "The-Wonderful-Wizard-of-Oz.txt",
        "The-Picture-of-Dorian-Gray.txt",
        "Around-the-World-in-80-Days.txt",
        "The-Jungle-Book.txt",
        "Jane-Eyre.txt",
        "The-Count-of-Monte-Cristo-Vol.-1.txt",
        # "Les-Miserables-Vol.-1.txt",
        "Moby-Dick.txt",
        "David-Copperfield.txt",
        "War-and-Peace-Vol.-1.txt",
        "Clarissa-Volume-1.txt",
        "In-Search-of-Lost-Time-Swanns-Way.txt"
    ]
    # Nice colors for the plots 
    colors = ['#1f77b4',  # muted blue
            '#ff7f0e',  # safety orange
            '#2ca02c',  # cooked asparagus green
            '#d62728',  # brick red
            '#9467bd',  # muted purple
            '#8c564b',  # chestnut brown
            '#e377c2',  # raspberry yogurt pink
            '#7f7f7f',  # middle gray
            '#bcbd22',  # curry yellow-green
            '#17becf']  # blue-teal
    # Generating the full path for each book and storing them in a list
    filenames = [dir_path / book for book in books]

    # Intilizing a figure object with 1 colums and 3 rows 
    fig, ax = plt.subplots(ncols=4, nrows=5, figsize=(20,16))
    # Flatten the ax object array in order to iterate it within the books loop 
    ax = ax.flatten()
    # Iterating over the books 
    for i, filename in enumerate(filenames):
        # Counting  the occurance of words in the book 
        word_counts = count_words_nltk(filename)
        # Taking the count of occurance of each word and sorting them 
        # in an ascending  order 
        freqs = np.array(sorted(word_counts.values(), reverse=True))
        # Generating ranks for each count 
        ranks = np.arange(1, len(freqs) + 1)

        # Since power law package takes raw observation 
        # We regenerate the ranks reapated accoding to their coressponding count 
        repeated_ranks = np.repeat(ranks, freqs)
        
        # Now we fit the data using the powerlaw package 
        # Theory: https://arxiv.org/abs/0706.1062 :) 
        fit = powerlaw.Fit(repeated_ranks, discrete=True, verbose=False)
        # Getting the estimated alpha
        alpha = fit.alpha 
        # Getting the rank from which the distrubution begin the powerlaw behavior 
        xmin = fit.xmin
        # Getting the Kolmogorov-Smirnov distance between the empirical data and the powerlaw fit 
        D = fit.D

        # Creating a mask for the data starting from xmin 
        mask = ranks >= int(fit.xmin)           
        # Interpolating the masked ranks with the fitted power law 
        pdf_probs = fit.power_law.pdf(ranks[mask])   
        # Scaling the relative frequncies to get the count of occurances 
        pdf_counts = pdf_probs * len(repeated_ranks)         

        # Setting the labels 
        label_alpha = rf'$\hat{{\alpha}} = {alpha:.3f}$'
        label_xmin = rf'$x_{{min}} = {int(xmin)}$'
        label_D = rf'$D = {D:.3f}$'
        label_fit = rf'powerlaw fit'
        title = filename.name.replace('-', ' ').removesuffix(".txt") + f" [n={len(ranks)}]"
        
        # Plotting the empirical data  
        ax[i].loglog(ranks, freqs, color=colors[int(i % len(colors))], marker='o', linestyle='none', mfc='none', markersize=4, alpha=0.6, label="Empirical")
        # Plotting the fitted data using powerlaw 
        ax[i].loglog(ranks[mask], pdf_counts, linestyle="--", color="black", label=label_fit)
        # Visulising the xmin from which the powerlaw behavior starts 
        ax[i].axvline(x=xmin, color="red", ls="--", alpha=0.5, label=r"$x_{\mathrm{min}}$")
        # Adding the estimated alpha to the legend 
        ax[i].plot([], [], color=colors[int(i % len(colors))], marker='none', linestyle='none', mfc='none', markersize=4, alpha=0.6, label=label_alpha)
        # Adding the estimated KS distance to the legend 
        ax[i].plot([], [], color=colors[int(i % len(colors))], marker='none', linestyle='none', mfc='none', markersize=4, alpha=0.6)
        # Adding a red xmin marker 
        # ax[i].text(xmin, ax[i].get_ylim()[0], r"$x_{\mathrm{min}}$", 
        #    color="red", ha="center", va="bottom")

        
        ax[i].set_xlabel("Rank", fontsize=8, labelpad=4)
        ax[i].set_ylabel("Frequency", fontsize=8, labelpad=4)
        ax[i].grid(True, which="both", ls="--", lw=0.5)
        ax[i].set_xlim(1E0, 1E4)
        ax[i].set_ylim(1E0, )
        ax[i].set_title(title, fontsize=8, pad=6)
        ax[i].legend(frameon=True, edgecolor="black", shadow=True, title="", title_fontsize="large")
    plt.subplots_adjust(top=0.93, bottom=0.05, left=0.07, right=0.97, hspace=0.45, wspace=0.3)    
    plt.tight_layout()
    # Save figure
    out_figure.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_figure)
    plt.show()
    print(f"Figure saved to: {out_figure}")

if __name__ == "__main__":
    main()
