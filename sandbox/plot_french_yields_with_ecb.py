import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path().resolve()

data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'french_govt_bond_yields.pkl')

column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_decision_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

# Initialize new column with zeros
data["10y Yield - 3dWindow"] = 0
data["10y Yield - Outside 3dWindow Change"] = data["10 Yield"].diff()

data.index = pd.to_datetime(data.index)

# Iterate over the dates in mpdd
for date in mpdd["MP Dates"]:    
    # Set the values for the 3-day window in the new column
    data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "10y Yield - 3dWindow Change"] = data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "10y Yield"].diff()
    data.loc[date - pd.Timedelta(days=3):date + pd.Timedelta(days=3), "10y Yield - 7dWindow Change"] = data.loc[date - pd.Timedelta(days=3):date + pd.Timedelta(days=3), "10y Yield"].diff()
    data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "10y Yield - Outside 3dWindow Change"] = np.nan


# ===============================================================================
# Plot 10y Treasury yield over time
# ===============================================================================
d3_data = data["10y Yield"].resample('3D').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(d3_data.index, d3_data)
plt.title("10y French Government Bond Yield")
plt.tight_layout()
plt.show()

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10y Yield Change"] = data["10y Yield"].diff().cumsum()
data["10y Yield - 3dWindow Change"] = data["10y Yield - 3dWindow Change"].cumsum()
data["10y Yield - 3dWindow Change"] = data["10y Yield - 3dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change"], label="10y Treasury yield", color="dimgrey")
plt.plot(data.index, data["10y Yield - 3dWindow Change"], label="10y Treasury yield change around ECB meetings", color="red")
plt.title("3-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'FR_ECB_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change w.r.t. 7-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10y Yield - 7dWindow Change"] = data["10y Yield - 7dWindow Change"].cumsum()
data["10y Yield - 7dWindow Change"] = data["10y Yield - 7dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change"], label="10y Treasury yield", color="dimgrey")
plt.plot(data.index, data["10y Yield - 7dWindow Change"], label="10y Treasury yield change around ECB meetings", color="red")
plt.title("7-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()

# ===============================================================================
# Outside 3-day windows around ECB meetings
# ===============================================================================

# Calculate the cumulative sum of these changes
data["10y Yield - Outside 3dWindow Change"] = data["10y Yield - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change"], label="10y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10y Yield - Outside 3dWindow Change"], label="10y Treasury yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 3-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'FR_ECB_10y_yield_outside-window_cumulative_change.png')
plt.show()