#!/usr/bin/env python3
import numpy as np
import powerlaw
import matplotlib.pyplot as plt
import contextlib
import sys
import os
from pathlib import Path

@contextlib.contextmanager
def suppress_stdout():
    """Context manager to suppress stdout output."""
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

def generate_synthetic_powerlaw_data(data, alpha, xmin, n_synthetic):
    """
    Generate synthetic data using Clauset's semiparametric bootstrap method.
    
    Parameters:
    -----------
    data : np.ndarray
        Original empirical data
    alpha : float
        Power-law exponent (fitted from empirical data)
    xmin : int
        Lower bound of power-law regime
    n_synthetic : int
        Number of synthetic data points to generate
    
    Returns:
    --------
    np.ndarray : Synthetic dataset
    """
    # Get the body (data < xmin) and tail size
    body_data = data[data < xmin]
    tail_data = data[data >= xmin]
    n_tail = len(tail_data)
    n_body = len(body_data)
    
    # If we want to maintain the same data structure, keep the same proportions
    if n_synthetic is None:
        n_synthetic = len(data)
    
    # Calculate proportion of tail data
    tail_proportion = n_tail / len(data)
    n_synthetic_tail = int(n_synthetic * tail_proportion)
    n_synthetic_body = n_synthetic - n_synthetic_tail
    
    synthetic_data = []
    
    # Generate synthetic body data by resampling from original body
    if n_synthetic_body > 0 and len(body_data) > 0:
        synthetic_body = np.random.choice(body_data, size=n_synthetic_body, replace=True)
        synthetic_data.extend(synthetic_body)
    
    # Generate synthetic tail data from power-law distribution
    if n_synthetic_tail > 0:
        # Use the inverse transform method for discrete power-law
        # For discrete power-law: P(X = k) ∝ k^(-alpha) for k >= xmin
        u = np.random.random(n_synthetic_tail)
        synthetic_tail = (xmin - 0.5) * (1 - u) ** (-1 / (alpha - 1))
        synthetic_tail = np.round(synthetic_tail).astype(int)
        synthetic_data.extend(synthetic_tail)
    
    return np.array(synthetic_data)

def compute_gof_pvalue(data, alpha=None, xmin=None, num_sims=2500, verbose=True):
    """
    Compute goodness-of-fit p-value for power-law hypothesis using Clauset's method.
    
    Parameters:
    -----------
    data : np.ndarray
        Empirical data
    alpha : float, optional
        Power-law exponent. If None, will be fitted from data.
    xmin : int, optional
        Lower bound of power-law regime. If None, will be fitted from data.
    num_sims : int
        Number of Monte Carlo simulations
    verbose : bool
        Whether to print progress
    
    Returns:
    --------
    dict : Dictionary containing p-value and other statistics
    """
    
    # Fit power-law to empirical data if parameters not provided
    if alpha is None or xmin is None:
        if verbose:
            print("Fitting power-law to empirical data...")
        
        with suppress_stdout():
            fit = powerlaw.Fit(data, discrete=True, verbose=False)
        
        if alpha is None:
            alpha = fit.power_law.alpha
        if xmin is None:
            xmin = fit.power_law.xmin
        
        empirical_ks = fit.power_law.D
    else:
        # If parameters provided, compute KS distance manually
        # This is useful when testing against theoretical values
        tail_data = data[data >= xmin]
        n_tail = len(tail_data)
        
        # Compute empirical CDF
        unique_vals = np.unique(tail_data)
        empirical_cdf = np.zeros(len(unique_vals))
        for i, val in enumerate(unique_vals):
            empirical_cdf[i] = np.sum(tail_data <= val) / n_tail
        
        # Compute theoretical power-law CDF
        zeta = np.sum(np.arange(xmin, max(tail_data) + 1) ** (-alpha))
        theoretical_cdf = np.zeros(len(unique_vals))
        for i, val in enumerate(unique_vals):
            theoretical_cdf[i] = np.sum(np.arange(xmin, val + 1) ** (-alpha)) / zeta
        
        empirical_ks = np.max(np.abs(empirical_cdf - theoretical_cdf))
    
    if verbose:
        print(f"Fitted parameters:")
        print(f"  alpha = {alpha:.4f}")
        print(f"  xmin = {xmin}")
        print(f"  KS distance = {empirical_ks:.4f}")
        print(f"\nRunning {num_sims} Monte Carlo simulations...")
    
    # Monte Carlo simulation
    ks_synthetic = []
    
    for sim in range(num_sims):
        if verbose and sim % 100 == 0:
            print(f"  Simulation {sim + 1}/{num_sims}", end='\r')
        
        # Generate synthetic data
        synthetic_data = generate_synthetic_powerlaw_data(data, alpha, xmin, len(data))
        
        # Fit power-law to synthetic data
        with suppress_stdout():
            synthetic_fit = powerlaw.Fit(synthetic_data, discrete=True, verbose=False)
        
        ks_synthetic.append(synthetic_fit.power_law.D)
    
    if verbose:
        print()  # New line after progress
    
    ks_synthetic = np.array(ks_synthetic)
    
    # Compute p-value
    p_value = np.mean(ks_synthetic > empirical_ks)
    
    results = {
        'p_value': p_value,
        'alpha': alpha,
        'xmin': xmin,
        'empirical_ks': empirical_ks,
        'synthetic_ks': ks_synthetic,
        'num_sims': num_sims
    }
    
    return results

def plot_gof_results(results, save_path=None):
    """Plot histogram of synthetic KS statistics vs empirical KS."""
    plt.figure(figsize=(10, 6))
    
    # Plot histogram
    plt.hist(results['synthetic_ks'], bins=50, alpha=0.7, color='skyblue', 
             label=f'Synthetic KS (n={results["num_sims"]})')
    
    # Plot empirical KS as vertical line
    plt.axvline(results['empirical_ks'], color='red', linestyle='--', linewidth=2,
                label=f'Empirical KS = {results["empirical_ks"]:.4f}')
    
    # Add p-value text
    plt.text(0.05, 0.95, f'p-value = {results["p_value"]:.4f}', 
             transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.xlabel('KS Statistic')
    plt.ylabel('Frequency')
    plt.title('Monte Carlo Goodness-of-Fit Test for Power-Law Hypothesis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        pass 
        # plt.savefig(save_path, dpi=300, bbox_inches='tight')
        # print(f"Figure saved to: {save_path}")
    
    plt.show()

def main():
    """Main function demonstrating the corrected power-law goodness-of-fit test."""
    
    # Example 1: Load data from file
    try:
        # Try to load the Zipf data mentioned in the original code
        filename = Path("data/raw/figure1/input_1.5.txt")
        if os.path.exists(filename):
            data = np.loadtxt(filename, dtype=int)
            print(f"Loaded data from {filename}")
        else:
            # Generate synthetic data for demonstration
            print("Data file not found. Generating synthetic power-law data for demonstration...")
            np.random.seed(42)
            # Generate synthetic power-law data with known parameters
            true_alpha = 2.5
            true_xmin = 10
            n_samples = 5000
            
            # Generate power-law tail
            u = np.random.random(n_samples)
            tail_data = (true_xmin - 0.5) * (1 - u) ** (-1 / (true_alpha - 1))
            tail_data = np.round(tail_data).astype(int)
            
            # Add some body data
            body_data = np.random.randint(1, true_xmin, size=2000)
            data = np.concatenate([body_data, tail_data])
            
            print(f"Generated synthetic data with alpha={true_alpha}, xmin={true_xmin}")
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    print(f"Data size: {len(data)}")
    print(f"Data range: [{np.min(data)}, {np.max(data)}]")
    
    # Test 1: Fit parameters from data (standard approach)
    print("\n" + "="*50)
    print("TEST 1: Fitting parameters from empirical data")
    print("="*50)
    
    results1 = compute_gof_pvalue(data, num_sims=1000)
    
    print(f"\nResults:")
    print(f"  p-value = {results1['p_value']:.4f}")
    
    if results1['p_value'] > 0.1:
        print("  ✅ The power-law hypothesis is plausible (p > 0.1)")
    else:
        print("  ❌ The power-law hypothesis can be rejected (p ≤ 0.1)")
    
    # Test 2: Test against theoretical values (if you have them)
    print("\n" + "="*50)
    print("TEST 2: Testing against theoretical parameters")
    print("="*50)
    
    # Example: test against theoretical alpha = 2.0
    theoretical_alpha = 2.0
    results2 = compute_gof_pvalue(data, alpha=theoretical_alpha, num_sims=1000)
    
    print(f"\nResults for theoretical alpha = {theoretical_alpha}:")
    print(f"  p-value = {results2['p_value']:.4f}")
    
    if results2['p_value'] > 0.1:
        print(f"  ✅ The theoretical alpha = {theoretical_alpha} is plausible")
    else:
        print(f"  ❌ The theoretical alpha = {theoretical_alpha} can be rejected")
    
    # Plot results
    print("\nPlotting results...")
    plot_gof_results(results1)

if __name__ == "__main__":
    main()