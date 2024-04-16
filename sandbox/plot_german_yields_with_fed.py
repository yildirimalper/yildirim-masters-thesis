import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()

data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'german_govt_bond_yields.pkl')
data.set_index('Date', inplace=True)
data.index = pd.to_datetime(data.index)
#! Since the earliest ECB meeting is 1999-03-04
cutoff_date = pd.to_datetime('1999-01-01')
data = data[data.index >= cutoff_date]

column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/fomc_meeting_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

# Apply this function to the "MP Dates" column of the `mpdd` DataFrame to create new columns
mpdd["3dWindow"] = mpdd["MP Dates"].apply(create_3d_window)
mpdd["5dWindow"] = mpdd["MP Dates"].apply(create_5d_window)
mpdd["7dWindow"] = mpdd["MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
three_day_windows = pd.Series([date for sublist in mpdd["3dWindow"] for date in sublist])
five_day_windows = pd.Series([date for sublist in mpdd["5dWindow"] for date in sublist])
seven_day_windows = pd.Series([date for sublist in mpdd["7dWindow"] for date in sublist])

# Create a new column in the `data` DataFrame that indicates whether each date is within a three-day window.
data["In 3dWindow"] = data.index.isin(three_day_windows)
data["In 5dWindow"] = data.index.isin(five_day_windows)
data["In 7dWindow"] = data.index.isin(seven_day_windows)

# Calculate the "10y Yield" change for each date in the `data` DataFrame.
data["10y Yield Change"] = data["10y Yield"].diff()

data["10y Yield - 3dWindow Change"] = data["10y Yield Change"].where(data["In 3dWindow"], 0)
data["10y Yield - 5dWindow Change"] = data["10y Yield Change"].where(data["In 5dWindow"], 0)
data["10y Yield - 7dWindow Change"] = data["10y Yield Change"].where(data["In 7dWindow"], 0)

data["10y Yield - Outside 3dWindow Change"] = data["10y Yield Change"].where(~data["In 3dWindow"], 0)
data["10y Yield - Outside 5dWindow Change"] = data["10y Yield Change"].where(~data["In 5dWindow"], 0)
data["10y Yield - Outside 7dWindow Change"] = data["10y Yield Change"].where(~data["In 7dWindow"], 0)

# ===============================================================================
# Plot 10y German Bund yield over time
# ===============================================================================
d3_data = data["10y Yield"].resample('3D').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(d3_data.index, d3_data)
plt.title("10y German Bund Yield")
plt.tight_layout()
plt.show()

# ===============================================================================
# Plot 10y German Bund Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10y Yield Change Cumulative"] = data["10y Yield"].diff().cumsum()
data["10y Yield - 3dWindow Change Cumulative"] = data["10y Yield - 3dWindow Change"].cumsum()
data["10y Yield - 3dWindow Change Cumulative"] = data["10y Yield - 3dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey")
plt.plot(data.index, data["10y Yield - 3dWindow Change Cumulative"], label="10y German Bund yield change around ECB meetings", color="red")
plt.title("3-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_3d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 3-day windows around ECB meetings
# ===============================================================================
data["10y Yield - Outside 3dWindow Change Cumulative"] = data["10y Yield - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10y Yield - Outside 3dWindow Change Cumulative"], label="10y German Bund yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 3-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_3d_10y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# 5-day inside window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10y Yield Change Cumulative"] = data["10y Yield"].diff().cumsum()
data["10y Yield - 5dWindow Change Cumulative"] = data["10y Yield - 5dWindow Change"].cumsum()
data["10y Yield - 5dWindow Change Cumulative"] = data["10y Yield - 5dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey")
plt.plot(data.index, data["10y Yield - 5dWindow Change Cumulative"], label="10y German Bund yield change around ECB meetings", color="red")
plt.title("5-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_5d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# 5-day outside window
# ===============================================================================
data["10y Yield - Outside 5dWindow Change Cumulative"] = data["10y Yield - Outside 5dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10y Yield - Outside 5dWindow Change Cumulative"], label="10y German Bund yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 5-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_5d_10y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# 7-day inside window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10y Yield Change Cumulative"] = data["10y Yield"].diff().cumsum()
data["10y Yield - 7dWindow Change Cumulative"] = data["10y Yield - 7dWindow Change"].cumsum()
data["10y Yield - 7dWindow Change Cumulative"] = data["10y Yield - 7dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey")
plt.plot(data.index, data["10y Yield - 7dWindow Change Cumulative"], label="10y German Bund yield change around ECB meetings", color="red")
plt.title("7-day windows around ECB meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_7d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# 7-day outside window
# ===============================================================================
data["10y Yield - Outside 7dWindow Change Cumulative"] = data["10y Yield - Outside 7dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10y Yield Change Cumulative"], label="10y German Bund yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10y Yield - Outside 7dWindow Change Cumulative"], label="10y German Bund yield change outside of ECB window", color="silver", alpha=0.9)
plt.title("Days outside 7-day ECB window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'german_bonds' / 'DE_ecb_7d_10y_yield_outside-window_cumulative_change.png')
plt.show()
