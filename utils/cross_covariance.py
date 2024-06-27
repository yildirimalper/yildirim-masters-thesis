import numpy as np

def cross_covariance(x, y, lag=0):
    """
    Compute the cross-covariance between two time series x and y at a given lag.
    
    Parameters:
    x (array-like): First time series.
    y (array-like): Second time series.
    lag (int): The lag at which to compute the cross-covariance (default is 0).
    
    Returns:
    float: Cross-covariance at the given lag.
    """
    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Adjust the series based on the lag
    if lag > 0:
        x_lagged = x[lag:]
        y_lagged = y[:n-lag]
    elif lag < 0:
        x_lagged = x[:n+lag]
        y_lagged = y[-lag:]
    else:
        x_lagged = x
        y_lagged = y
    
    covariance = np.mean((x_lagged - mean_x) * (y_lagged - mean_y))
    return covariance