import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'japanese_spot_yields.pkl')

column_names = ["BoJ MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/boj_mpd.csv", header=None, names=column_names)
mpdd["BoJ MP Dates"] = pd.to_datetime(mpdd["BoJ MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Convert the index to datetime and filter the data first
data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
data = data.loc[data.index >= '1999-01-01']

# For BoJ
mpdd["BoJ 3dWindow"] = mpdd["BoJ MP Dates"].apply(create_3d_window)
mpdd["BoJ 5dWindow"] = mpdd["BoJ MP Dates"].apply(create_5d_window)
mpdd["BoJ 7dWindow"] = mpdd["BoJ MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
boj_three_day_windows = pd.Series([date for sublist in mpdd["BoJ 3dWindow"] for date in sublist])
boj_five_day_windows = pd.Series([date for sublist in mpdd["BoJ 5dWindow"] for date in sublist])
boj_seven_day_windows = pd.Series([date for sublist in mpdd["BoJ 7dWindow"] for date in sublist])

# For Fed
fed_mpdd["Fed 3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["Fed 5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["Fed 7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 7dWindow"] for date in sublist])

# Create new columns in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In BoJ 3dWindow"] = data.index.isin(boj_three_day_windows)
data["In BoJ 5dWindow"] = data.index.isin(boj_five_day_windows)
data["In BoJ 7dWindow"] = data.index.isin(boj_seven_day_windows)

data["In Fed 3dWindow"] = data.index.isin(fed_three_day_windows)
data["In Fed 5dWindow"] = data.index.isin(fed_five_day_windows)
data["In Fed 7dWindow"] = data.index.isin(fed_seven_day_windows)

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

# For BoJ
data["BoJ 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In BoJ 3dWindow"], 0)
data["BoJ 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In BoJ 5dWindow"], 0)
data["BoJ 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In BoJ 7dWindow"], 0)

data["BoJ 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In BoJ 3dWindow"], 0)
data["BoJ 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In BoJ 5dWindow"], 0)
data["BoJ 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In BoJ 7dWindow"], 0)

# For Fed
data["Fed 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In Fed 3dWindow"], 0)
data["Fed 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In Fed 5dWindow"], 0)
data["Fed 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In Fed 7dWindow"], 0)

data["Fed 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_japanese_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_japanese_spot_yields.pkl')

# ===============================================================================
# Plot 10y Japanese Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["BoJ 10yr - 3dWindow Change Cumulative"] = data["BoJ 10yr - 3dWindow Change"].cumsum()
data["BoJ 10yr - 3dWindow Change Cumulative"] = data["BoJ 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y UK gilt yield", color="dimgrey")
plt.plot(data.index, data["BoJ 10yr - 3dWindow Change Cumulative"], label="10y Japanese bond yield change around the BoJ meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y Japanese bond yield change around the Fed meetings", color="red")
plt.title("3-day windows around the BoJ and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()