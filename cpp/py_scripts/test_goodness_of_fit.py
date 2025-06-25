# /bin/bash/env python3 

import numpy as np 
import powerlaw
import contextlib
import sys
import os
"""
There is an issue with the logic of this code that I have to understand 
the p-value is computed against the estimated exponent and not the theortical value 
I have to figure this out. I think it is not canonical to the point of the paper
But it is an intresting idea to investigate. 
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
def generate_semiparametric(data:np.ndarray, xmin:int, alpha:float, n:int, ntail:int):
    """Generate one synthetic dataset using Clauset's semiparametric bootstrap."""
    # Split data into body and tail
    body = data[data < xmin]
    p_tail = ntail / n
    synthetic_data = []

    for _ in range(n):
        if np.random.rand() < p_tail:
            # Generate from power-law above xmin
            xi = powerlaw.Power_Law(xmin=xmin, parameters=[alpha], discrete=True).generate_random(1)[0]
        else:
            # Sample from empirical body
            xi = np.random.choice(body)
        synthetic_data.append(xi)
    return np.array(synthetic_data)

def get_p_val(data:np.ndarray, xmin:int, alpha:float, empirical_ks:float,n:int, num_sims:int=10):
    """
    A function to compute the p-values for the power law fit based on the mechanism described in section 4 in 
    https://arxiv.org/abs/0706.1062
    """
    ntail = np.sum(data >= xmin)
    # List to store the KS distances between the synthetic data and their power law fit
    ks_stats = []
    # Generate num_sims synthetic data sets
    for sim in range(num_sims):
        # Print the progress 
        print(f"Simulation: {sim} / {num_sims} ...", end="\r")
        # Generate synthetic power-law data with same alpha and xmin
        synthetic_data = generate_semiparametric(data, xmin, alpha, n, ntail)

        # Fit synthetic data to a power-law
        with suppress_stdout():
            synthetic_fit = powerlaw.Fit(synthetic_data, discrete=True, verbose=False)
        synthetic_ks = synthetic_fit.power_law.D
        ks_stats.append(synthetic_ks)
    # Compute p-value
    ks_stats = np.array(ks_stats)
    # The p-value is the fraction of distances that are larger than the KS distance
    # Between the empirical data and the power law model 
    p_value = np.mean(ks_stats > empirical_ks)
    return p_value


def main():
    for mu in [2.0]:
        desired_precison = float(0.1)
        n_sims = int(0.25 / (desired_precison * desired_precison)) 
        filename = f"./data/figure1/input_{mu}.txt"
        print(f"Processing file {filename}")
        data = np.loadtxt(filename, dtype=int)

        n = int(1E3)
        data = data[:n]  
        # Using only the first 1000 points of the simulation to test the goodness of fit  
        print(f"Testing the power law fittness using {n} data points")
        with suppress_stdout():
            fit = powerlaw.Fit(data, discrete=True, verbose=False)
        alpha = mu # The hypothesized value of the exponent 
                        # a power law 
        D = fit.D
        xmin = fit.xmin 

        print(f"Estimated alpha: {alpha}")
        print(f"Estimated xmin: {xmin}")
        print(f"KS distance: {D}")

        p_val = get_p_val(data, xmin, alpha, D,n, n_sims)
        print(f"\nEstimated p-value: {p_val:.2f}\n")
    
if __name__ == "__main__":
    main()