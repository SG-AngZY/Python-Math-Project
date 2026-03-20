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
    def binomial_p_value(k, n, p, test_type="two-tail"):
        """Calculates the p-value for a binomial test."""
        if test_type == "equal":
            # Just the probability of exactly k
            return binom.pmf(k, n, p)
        elif test_type == "left-tail":
            return binom.cdf(k, n, p)
        elif test_type == "right-tail":
            # P(X >= k) = 1 - P(X <= k-1)
            return 1 - binom.cdf(k - 1, n, p)
        else:
            # Two-tail: Sum probabilities of all outcomes as likely or less likely than observed
            obs_prob = binom.pmf(k, n, p)
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
    def normal_p_value(x, mu, sigma, test_type="two-tail"):
        """Calculates the p-value for a normal distribution test."""
        prob_left = norm.cdf(x, mu, sigma)
        
        if test_type == "left-tail":
            return prob_left
        elif test_type == "right-tail":
            return 1 - prob_left
        else:  # two-tail
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