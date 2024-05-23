import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'spot_yields.pkl')
data.index = pd.to_datetime(data.index)

column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_decision_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/fomc_meeting_dates.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Apply this function to the "MP Dates" column of the `mpdd` DataFrame to create new columns
mpdd["3dWindow"] = mpdd["MP Dates"].apply(create_3d_window)
mpdd["5dWindow"] = mpdd["MP Dates"].apply(create_5d_window)
mpdd["7dWindow"] = mpdd["MP Dates"].apply(create_7d_window)

# Apply the same transformations to the Fed dates
fed_mpdd["3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
three_day_windows = pd.Series([date for sublist in mpdd["3dWindow"] for date in sublist])
five_day_windows = pd.Series([date for sublist in mpdd["5dWindow"] for date in sublist])
seven_day_windows = pd.Series([date for sublist in mpdd["7dWindow"] for date in sublist])

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["7dWindow"] for date in sublist])

# Combine the ECB and Fed dates
combined_three_day_windows = pd.concat([three_day_windows, fed_three_day_windows])
combined_five_day_windows = pd.concat([five_day_windows, fed_five_day_windows])
combined_seven_day_windows = pd.concat([seven_day_windows, fed_seven_day_windows])

# Create a new column in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In 3dWindow"] = data.index.isin(combined_three_day_windows)
data["In 5dWindow"] = data.index.isin(combined_five_day_windows)
data["In 7dWindow"] = data.index.isin(combined_seven_day_windows)

# Calculate the "YC - Spot - 10y" change for each date in the `data` DataFrame.
data["YC - Spot - 10y Change"] = data["YC - Spot - 10y"].diff()

data["YC - Spot - 10y - 3dWindow Change"] = data["YC - Spot - 10y Change"].where(data["In 3dWindow"], 0)
data["YC - Spot - 10y - 5dWindow Change"] = data["YC - Spot - 10y Change"].where(data["In 5dWindow"], 0)
data["YC - Spot - 10y - 7dWindow Change"] = data["YC - Spot - 10y Change"].where(data["In 7dWindow"], 0)

data["YC - Spot - 10y - Outside 3dWindow Change"] = data["YC - Spot - 10y Change"].where(~data["In 3dWindow"], 0)
data["YC - Spot - 10y - Outside 5dWindow Change"] = data["YC - Spot - 10y Change"].where(~data["In 5dWindow"], 0)
data["YC - Spot - 10y - Outside 7dWindow Change"] = data["YC - Spot - 10y Change"].where(~data["In 7dWindow"], 0)

# ===============================================================================
# Plot 10y yield over time
# ===============================================================================
d3_data = data["YC - Spot - 10y"].resample('3D').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(d3_data.index, d3_data)
plt.title("10y AAA-rated European Bond Yield")
plt.tight_layout()
plt.show()

# ===============================================================================
# Plot 10y European Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["YC - Spot - 10y Change Cumulative"] = data["YC - Spot - 10y"].diff().cumsum()
data["YC - Spot - 10y - 3dWindow Change Cumulative"] = data["YC - Spot - 10y - 3dWindow Change"].cumsum()
data["YC - Spot - 10y - 3dWindow Change Cumulative"] = data["YC - Spot - 10y - 3dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 10y - 3dWindow Change Cumulative"], label="10y AAA-rated European bond yield change around ECB and Fed meetings", color="red")
plt.title("3-day windows around ECB and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_3d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 3-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 10y - Outside 3dWindow Change Cumulative"] = data["YC - Spot - 10y - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 10y - Outside 3dWindow Change Cumulative"], label="10y AAA-rated European bond yield change outside of ECB and Fed windows", color="silver", alpha=0.9)
plt.title("Days outside 3-day ECB and Fed windows", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_3d_10y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change w.r.t. 5-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes for the 5-day window
data["YC - Spot - 10y - 5dWindow Change Cumulative"] = data["YC - Spot - 10y - 5dWindow Change"].cumsum()
data["YC - Spot - 10y - 5dWindow Change Cumulative"] = data["YC - Spot - 10y - 5dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 10y - 5dWindow Change Cumulative"], label="10y AAA-rated European bond yield change around ECB and Fed meetings", color="red")
plt.title("5-day windows around ECB and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_5d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 5-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 10y - Outside 5dWindow Change Cumulative"] = data["YC - Spot - 10y - Outside 5dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 10y - Outside 5dWindow Change Cumulative"], label="10y AAA-rated European bond yield change outside of ECB and Fed windows", color="silver", alpha=0.9)
plt.title("Days outside 5-day ECB and Fed windows", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_5d_10y_yield_outside-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change w.r.t. 7-day window
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["YC - Spot - 10y - 7dWindow Change Cumulative"] = data["YC - Spot - 10y - 7dWindow Change"].cumsum()
data["YC - Spot - 10y - 7dWindow Change Cumulative"] = data["YC - Spot - 10y - 7dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey")
plt.plot(data.index, data["YC - Spot - 10y - 7dWindow Change Cumulative"], label="10y AAA-rated European bond yield change around ECB and Fed meetings", color="red")
plt.title("7-day windows around ECB and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_7d_10y_yield_in-window_cumulative_change.png')
plt.show()

# ===============================================================================
# Outside 7-day windows around ECB meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["YC - Spot - 10y - Outside 7dWindow Change Cumulative"] = data["YC - Spot - 10y - Outside 7dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["YC - Spot - 10y Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["YC - Spot - 10y - Outside 7dWindow Change Cumulative"], label="10y AAA-rated European bond yield change outside of ECB and Fed windows", color="silver", alpha=0.9)
plt.title("Days outside 7-day ECB and Fed windows", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'ecb+fed_7d_10y_yield_outside-window_cumulative_change.png')
plt.show()

# Export data
data.to_pickle(PROJECT_DIR / 'processed_data' / 'computed_10y_data_with_both.pkl')