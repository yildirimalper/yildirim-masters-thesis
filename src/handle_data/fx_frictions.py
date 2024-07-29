import pandas as pd
import numpy as np
from pathlib import Path
from utils.corwin_schultz import HLSpreadEstimator

PROJECT_DIR = Path().resolve()

# ==================================================
# USD-EUR exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdeur.csv')
data["Date"] = pd.to_datetime(data["Date"])

data["High"] = data["High"].str.replace(',', '.').astype(float)
data["Low"] = data["Low"].str.replace(',', '.').astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdeur_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdeur_with_spread.pkl')

# ==================================================
# USD-GBP exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdgbp.csv')
data["Date"] = pd.to_datetime(data["Date"])

# Ensure "High" and "Low" columns are of type float
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

# Save the updated DataFrame to a new CSV file
data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdgbp_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdgbp_with_spread.pkl')

# ==================================================
# USD-JPY exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdjpy.csv')
data["Date"] = pd.to_datetime(data["Date"])

# Ensure "High" and "Low" columns are of type float
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdjpy_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdjpy_with_spread.pkl')

# ==================================================
# USD-CAD exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdcad.csv')
data["Date"] = pd.to_datetime(data["Date"])

# Ensure "High" and "Low" columns are of type float
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdcad_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdcad_with_spread.pkl')

# ==================================================
# USD-CHF exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdchf.csv')
data["Date"] = pd.to_datetime(data["Date"])

# Ensure "High" and "Low" columns are of type float
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdchf_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdchf_with_spread.pkl')

# ==================================================
# USD-AUD exchange rates with spread estimation
# ==================================================

# Load your historical data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdaud.csv')
data["Date"] = pd.to_datetime(data["Date"])

# Ensure "High" and "Low" columns are of type float
data["High"] = data["High"].astype(float)
data["Low"] = data["Low"].astype(float)

# Initialize a list to store the spread values
spreads = [np.nan]  # First value is NaN because there's no previous day to compare

# Compute the spread for each pair of consecutive days
for i in range(1, len(data)):
    highs = data["High"].iloc[i-1:i+1].values
    lows = data["Low"].iloc[i-1:i+1].values
    spread = HLSpreadEstimator(highs, lows)
    spreads.append(spread)

# Add the spread values as a new column in the DataFrame
data["Spread"] = spreads

data.to_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdaud_with_spread.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdaud_with_spread.pkl')