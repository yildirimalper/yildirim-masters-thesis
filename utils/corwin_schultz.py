import pandas as pd
import numpy as np

def HLSpreadEstimator(highs, lows):
    beta = (np.log(highs[0] / lows[0]))**2 + (np.log(highs[1] / lows[1]))**2
    H = max(highs)
    L = min(lows)
    gamma = (np.log(H / L))**2
    alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / (3 - 2 * np.sqrt(2)) - np.sqrt(gamma / (3 - 2 * np.sqrt(2)))
    s = (2 * (np.exp(alpha) - 1)) / (1 + np.exp(alpha))
    s = max(s, 0)
    return s