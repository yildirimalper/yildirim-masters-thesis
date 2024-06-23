import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'canadian_spot_yields.pkl')

column_names = ["BoC MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/boc_mpd.csv", header=None, names=column_names)
mpdd["BoC MP Dates"] = pd.to_datetime(mpdd["BoC MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Convert the index to datetime and filter the data first
data.index = pd.to_datetime(data.index)
#data = data.loc[data.index >= '1999-01-01']
data = data.loc[data.index >= '2008-01-01']

# For BoC
mpdd["BoC 3dWindow"] = mpdd["BoC MP Dates"].apply(create_3d_window)
mpdd["BoC 5dWindow"] = mpdd["BoC MP Dates"].apply(create_5d_window)
mpdd["BoC 7dWindow"] = mpdd["BoC MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
boc_three_day_windows = pd.Series([date for sublist in mpdd["BoC 3dWindow"] for date in sublist])
boc_five_day_windows = pd.Series([date for sublist in mpdd["BoC 5dWindow"] for date in sublist])
boc_seven_day_windows = pd.Series([date for sublist in mpdd["BoC 7dWindow"] for date in sublist])

# For Fed
fed_mpdd["Fed 3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["Fed 5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["Fed 7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 7dWindow"] for date in sublist])

# Create new columns in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In BoC 3dWindow"] = data.index.isin(boc_three_day_windows)
data["In BoC 5dWindow"] = data.index.isin(boc_five_day_windows)
data["In BoC 7dWindow"] = data.index.isin(boc_seven_day_windows)

data["In Fed 3dWindow"] = data.index.isin(fed_three_day_windows)
data["In Fed 5dWindow"] = data.index.isin(fed_five_day_windows)
data["In Fed 7dWindow"] = data.index.isin(fed_seven_day_windows)

data.rename(columns={"10.0yr" : "10yr"}, inplace=True)
data['10yr'] = pd.to_numeric(data['10yr'], errors='coerce')

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

# For BoC
data["BoC 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In BoC 3dWindow"], 0)
data["BoC 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In BoC 5dWindow"], 0)
data["BoC 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In BoC 7dWindow"], 0)

data["BoC 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In BoC 3dWindow"], 0)
data["BoC 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In BoC 5dWindow"], 0)
data["BoC 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In BoC 7dWindow"], 0)

# For Fed
data["Fed 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In Fed 3dWindow"], 0)
data["Fed 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In Fed 5dWindow"], 0)
data["Fed 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In Fed 7dWindow"], 0)

data["Fed 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_canadian_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_canadian_spot_yields.pkl')

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
# Plot 10y Canadian Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["BoC 10yr - 3dWindow Change Cumulative"] = data["BoC 10yr - 3dWindow Change"].cumsum()
data["BoC 10yr - 3dWindow Change Cumulative"] = data["BoC 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y Canadian bond yield ", color="dimgrey")
plt.plot(data.index, data["BoC 10yr - 3dWindow Change Cumulative"], label="10y Canadian bond yield change around the BoC meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y Canadian bond yield change around the Fed meetings", color="red")
plt.title("3-day windows around the BoC and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'two_bank_figures' / '2008_canadian_bond_figure1a.png')
plt.show()