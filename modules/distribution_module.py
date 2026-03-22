import math
import numpy as np
from scipy.stats import binom, norm

class DistributionModule:
    """
    Core logic for Binomial and Normal distributions, 
    including Probability functions and Hypothesis Testing (p-values).
    """

    # --- BINOMIAL METHODS ---
    @staticmethod
    def binomial_pmf(k, n, p):
        """Probability of exactly k successes: P(X = k)"""
        return binom.pmf(k, n, p)

    @staticmethod
    def binomial_cdf(k, n, p):
        """Cumulative probability: P(X <= k)"""
        return binom.cdf(k, n, p)

    @staticmethod
    def binomial_p_value(n, p, test_type, k1, k2=None):
        """Calculates the p-value for a binomial test."""
        # Convert to appropriate types
        n = int(n)
        p = float(p)
        k1 = int(k1)

        if test_type == "left-tail":
            return binom.cdf(k1, n, p)
        
        elif test_type == "right-tail":
            # P(X >= k1) = 1 - P(X <= k1-1)
            return 1 - binom.cdf(k1 - 1, n, p)
        
        elif test_type == "middle":
            if k2 is None: return 0
            k2 = int(k2)
            # P(k1 <= X <= k2) = P(X <= k2) - P(X <= k1-1)
            return binom.cdf(k2, n, p) - binom.cdf(k1 - 1, n, p)
        
        else: # two-tail
            # Sum probabilities of all outcomes as likely or less likely than observed k1
            obs_prob = binom.pmf(k1, n, p)
            x = np.arange(0, n + 1)
            probs = binom.pmf(x, n, p)
            return np.sum(probs[probs <= obs_prob + 1e-9])

    # --- NORMAL METHODS ---
    @staticmethod
    def normal_pdf(x, mu, sigma):
        """Probability Density Function: The height of the bell curve at x."""
        return norm.pdf(x, mu, sigma)

    @staticmethod
    def normal_cdf(x, mu, sigma):
        """Cumulative Distribution Function: Area to the left of x."""
        return norm.cdf(x, mu, sigma)

    @staticmethod
    def normal_p_value(mu, sigma, test_type, k1, k2=None):
        """Calculates the p-value/area for normal distribution."""
        mu = float(mu)
        sigma = float(sigma)
        k1 = float(k1)

        if test_type == "left-tail":
            return norm.cdf(k1, mu, sigma)
        
        elif test_type == "right-tail":
            return 1 - norm.cdf(k1, mu, sigma)
        
        elif test_type == "middle":
            if k2 is None: return 0
            k2 = float(k2)
            # This gives you the 0.1359 result for P(10 <= X <= 20)
            return norm.cdf(k2, mu, sigma) - norm.cdf(k1, mu, sigma)
        
        else: # two-tail
            prob_left = norm.cdf(k1, mu, sigma)
            # Symmetry: 2 * the smaller of the two tail areas
            return 2 * min(prob_left, 1 - prob_left)

    # --- HELPER DATA GENERATORS ---
    @staticmethod
    def get_normal_range(mu, sigma, num_points=200):
        x = np.linspace(mu - 4*sigma, mu + 4*sigma, num_points)
        y = norm.pdf(x, mu, sigma)
        return x, y

    @staticmethod
    def get_binomial_range(n, p):
        x = np.arange(0, n + 1)
        y = binom.pmf(x, n, p)
        return x, y