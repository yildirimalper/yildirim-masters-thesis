import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path().resolve()

data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'spot_yields.pkl')

column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_decision_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

# Initialize new column with zeros
data["YC - Spot - 5y - 3dWindow"] = 0
data["YC - Spot - 5y - Outside 3dWindow Change"] = data["YC - Spot - 5y"].diff()
data["YC - Spot - 5y - 5dWindow"] = 0
data["YC - Spot - 5y - Outside 5dWindow Change"] = data["YC - Spot - 5y"].diff()
data["YC - Spot - 5y - 7dWindow"] = 0
data["YC - Spot - 5y - Outside 7dWindow Change"] = data["YC - Spot - 5y"].diff()
data["YC - Spot - 5y - 9dWindow"] = 0
data["YC - Spot - 5y - Outside 9dWindow Change"] = data["YC - Spot - 5y"].diff()

data.index = pd.to_datetime(data.index)

# Iterate over the dates in mpdd
for date in mpdd["MP Dates"]:    
    # Set the values for the 3-day window in the new column
    data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "YC - Spot - 5y - 3dWindow Change"] = data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "YC - Spot - 5y"].diff()
    data.loc[date - pd.Timedelta(days=1):date + pd.Timedelta(days=1), "YC - Spot - 5y - Outside 3dWindow Change"] = np.nan

    # Set the values for the 5-day window
    data.loc[date - pd.Timedelta(days=2):date + pd.Timedelta(days=2), "YC - Spot - 5y - 5dWindow Change"] = data.loc[date - pd.Timedelta(days=2):date + pd.Timedelta(days=2), "YC - Spot - 5y"].diff()
    data.loc[date - pd.Timedelta(days=2):date + pd.Timedelta(days=2), "YC - Spot - 5y - Outside 5dWindow Change"] = np.nan

    # Set the values for the 7-day window
    data.loc[date - pd.Timedelta(days=3):date + pd.Timedelta(days=3), "YC - Spot - 5y - 7dWindow Change"] = data.loc[date - pd.Timedelta(days=3):date + pd.Timedelta(days=3), "YC - Spot - 5y"].diff()
    data.loc[date - pd.Timedelta(days=3):date + pd.Timedelta(days=3), "YC - Spot - 5y - Outside 7dWindow Change"] = np.nan

    # Set the values for the 9-day window
    data.loc[date - pd.Timedelta(days=4):date + pd.Timedelta(days=4), "YC - Spot - 5y - 9dWindow Change"] = data.loc[date - pd.Timedelta(days=4):date + pd.Timedelta(days=4), "YC - Spot - 5y"].diff()
    data.loc[date - pd.Timedelta(days=4):date + pd.Timedelta(days=4), "YC - Spot - 5y - Outside 9dWindow Change"] = np.nan

# ===============================================================================
# Plot 5y Treasury yield over time
# ===============================================================================
d3_data = data["YC - Spot - 5y"].resample('3D').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(d3_data.index, d3_data)
plt.title("5y Treasury Yield")
plt.tight_layout()
plt.show()

# ===============================================================================
# Plot 5y Treasury Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["YC - Spot - 5y Change"] = data["YC - Spot - 5y"].diff().cumsum()
data["YC - Spot - 5y - 3dWindow Change"] = data["YC - Spot - 5y - 3dWindow Change"].cumsum()
data["YC - Spot - 5y - 3dWindow Change"] = data["YC - Spot - 5y - 3dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 5y - 3dWindow Change"], label="5y Treasury yield change around ECB meetings", color="red")
plt.title("3-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_3d_5y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 3-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 5y - Outside 3dWindow Change"] = data["YC - Spot - 5y - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 5y - Outside 3dWindow Change"], label="5y Treasury yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 3-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_3d_5y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 5y Treasury Cumulative Yield Change w.r.t. 5-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes for the 5-day window
data["YC - Spot - 5y - 5dWindow Change"] = data["YC - Spot - 5y - 5dWindow Change"].cumsum()
data["YC - Spot - 5y - 5dWindow Change"] = data["YC - Spot - 5y - 5dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 5y - 5dWindow Change"], label="5y Treasury yield change around ECB meetings", color="red")
plt.title("5-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_5d_5y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 5-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 5y - Outside 5dWindow Change"] = data["YC - Spot - 5y - Outside 5dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 5y - Outside 5dWindow Change"], label="5y Treasury yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 5-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_5d_5y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 5y Treasury Cumulative Yield Change w.r.t. 7-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["YC - Spot - 5y - 7dWindow Change"] = data["YC - Spot - 5y - 7dWindow Change"].cumsum()
data["YC - Spot - 5y - 7dWindow Change"] = data["YC - Spot - 5y - 7dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 5y - 7dWindow Change"], label="5y Treasury yield change around ECB meetings", color="red")
plt.title("7-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_7d_5y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 7-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 5y - Outside 7dWindow Change"] = data["YC - Spot - 5y - Outside 7dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 5y - Outside 7dWindow Change"], label="5y Treasury yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 7-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_7d_5y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 5y Treasury Cumulative Yield Change w.r.t. 9-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["YC - Spot - 5y - 9dWindow Change"] = data["YC - Spot - 5y - 9dWindow Change"].cumsum()
data["YC - Spot - 5y - 9dWindow Change"] = data["YC - Spot - 5y - 9dWindow Change"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 5y - 9dWindow Change"], label="5y Treasury yield change around ECB meetings", color="red")
plt.title("9-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_9d_5y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 9-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 5y - Outside 9dWindow Change"] = data["YC - Spot - 5y - Outside 9dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 5y Change"], label="5y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 5y - Outside 9dWindow Change"], label="5y Treasury yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 9-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb_9d_5y_yield_outside-window_cumulative_change.png')
plt.show()

