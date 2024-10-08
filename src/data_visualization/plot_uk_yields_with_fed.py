import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_spot_yields.pkl')

column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

# Convert the index to datetime and filter the data first
data.index = pd.to_datetime(data.index)
#data = data.loc[data.index >= '1989-01-01']
#data = data.loc[data.index >= '1997-06-01']
data = data.loc[data.index >= '2008-01-01']

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

data.rename(columns={"10.0yr" : "10yr"}, inplace=True)

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

data["10yr - 3dWindow Change"] = data["10yr Change"].where(data["In 3dWindow"], 0)
data["10yr - 5dWindow Change"] = data["10yr Change"].where(data["In 5dWindow"], 0)
data["10yr - 7dWindow Change"] = data["10yr Change"].where(data["In 7dWindow"], 0)

data["10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In 3dWindow"], 0)
data["10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In 5dWindow"], 0)
data["10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In 7dWindow"], 0)

# ===============================================================================
# Plot 10y yield over time
# ===============================================================================
d3_data = data["10yr"].resample('3D').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(d3_data.index, d3_data)
plt.title("10y UK Gilt Yield")
plt.tight_layout()
plt.show()

# ===============================================================================
# Plot 10y Australian Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["10yr - 3dWindow Change Cumulative"] = data["10yr - 3dWindow Change"].cumsum()
data["10yr - 3dWindow Change Cumulative"] = data["10yr - 3dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y UK gilt yield", color="dimgrey")
plt.plot(data.index, data["10yr - 3dWindow Change Cumulative"], label="10y UK gilt yield change around the Fed meetings", color="red")
plt.title("3-day windows around the Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_1989_yield_in-window_cumulative_change.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_1997_yield_in-window_cumulative_change.png')
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_2008_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 3-day windows around the FED meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["10yr - Outside 3dWindow Change Cumulative"] = data["10yr - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y UK gilt yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10yr - Outside 3dWindow Change Cumulative"], label="10y UK gilt yield change outside of FED window", color="silver", alpha=0.9)
plt.title("Days outside 3-day FED window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_1989_yield_outside-window_cumulative_change.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_1997_yield_outside-window_cumulative_change.png')
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_3d_10y_2008_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 10y Australian Cumulative Yield Change w.r.t. 5-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes for the 5-day window
data["10yr - 5dWindow Change Cumulative"] = data["10yr - 5dWindow Change"].cumsum()
data["10yr - 5dWindow Change Cumulative"] = data["10yr - 5dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], 
        label="10y UK gilt yield", color="dimgrey")
plt.plot(data.index, data["10yr - 5dWindow Change Cumulative"], 
        label="10y UK gilt yield change around the FED meetings", color="red")
plt.title("5-day windows around the FED meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_1989_yield_in-window_cumulative_change.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_1997_yield_in-window_cumulative_change.png')
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_2008_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 5-day windows around the FED meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["10yr - Outside 5dWindow Change Cumulative"] = data["10yr - Outside 5dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y UK gilt yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10yr - Outside 5dWindow Change Cumulative"], label="10y UK gilt yield change outside of the FED window", color="silver", alpha=0.9)
plt.title("Days outside 5-day FED window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_1989_yield_outside-window_cumulative_change.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_1997_yield_outside-window_cumulative_change.png')
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_5d_10y_2008_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change w.r.t. 7-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["10yr - 7dWindow Change Cumulative"] = data["10yr - 7dWindow Change"].cumsum()
data["10yr - 7dWindow Change Cumulative"] = data["10yr - 7dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], 
        label="10y UK gilt yield", color="dimgrey")
plt.plot(data.index, data["10yr - 7dWindow Change Cumulative"], 
        label="10y UK gilt yield change around the FED meetings", color="red")
plt.title("7-day windows around the FED meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed_7d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 7-day windows around the FED meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["10yr - Outside 7dWindow Change Cumulative"] = data["10yr - Outside 7dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], 
        label="10y UK gilt yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["10yr - Outside 7dWindow Change Cumulative"], 
        label="10y UK gilt yield change outside of the FED window", color="silver", alpha=0.9)
plt.title("Days outside 7-day FED window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figs' / 'boe_mpd' / 'fed__7d_10y_yield_outside-window_cumulative_change.png')
plt.show()