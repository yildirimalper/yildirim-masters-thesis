import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_spot_yields.pkl')

column_names = ["RBA MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/rba_mpd.csv", header=None, names=column_names)
mpdd["RBA MP Dates"] = pd.to_datetime(mpdd["RBA MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Convert the index to datetime and filter the data first
data.index = pd.to_datetime(data.index)
data = data.loc[data.index >= '2008-01-01']

data.rename(columns={"10yr - AG" : "10yr"}, inplace=True)

# For RBA
mpdd["RBA 3dWindow"] = mpdd["RBA MP Dates"].apply(create_3d_window)
mpdd["RBA 5dWindow"] = mpdd["RBA MP Dates"].apply(create_5d_window)
mpdd["RBA 7dWindow"] = mpdd["RBA MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
rba_three_day_windows = pd.Series([date for sublist in mpdd["RBA 3dWindow"] for date in sublist])
rba_five_day_windows = pd.Series([date for sublist in mpdd["RBA 5dWindow"] for date in sublist])
rba_seven_day_windows = pd.Series([date for sublist in mpdd["RBA 7dWindow"] for date in sublist])

# For Fed
fed_mpdd["Fed 3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["Fed 5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["Fed 7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 7dWindow"] for date in sublist])

# Create new columns in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In RBA 3dWindow"] = data.index.isin(rba_three_day_windows)
data["In RBA 5dWindow"] = data.index.isin(rba_five_day_windows)
data["In RBA 7dWindow"] = data.index.isin(rba_seven_day_windows)

data["In Fed 3dWindow"] = data.index.isin(fed_three_day_windows)
data["In Fed 5dWindow"] = data.index.isin(fed_five_day_windows)
data["In Fed 7dWindow"] = data.index.isin(fed_seven_day_windows)

data.rename(columns={"10.0yr" : "10yr"}, inplace=True)

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

# For RBA
data["RBA 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In RBA 3dWindow"], 0)
data["RBA 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In RBA 5dWindow"], 0)
data["RBA 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In RBA 7dWindow"], 0)

data["RBA 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In RBA 3dWindow"], 0)
data["RBA 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In RBA 5dWindow"], 0)
data["RBA 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In RBA 7dWindow"], 0)

# For Fed
data["Fed 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In Fed 3dWindow"], 0)
data["Fed 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In Fed 5dWindow"], 0)
data["Fed 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In Fed 7dWindow"], 0)

data["Fed 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_australian_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_australian_spot_yields.pkl')

# ===============================================================================
# Plot 10y Australian Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["RBA 10yr - 3dWindow Change Cumulative"] = data["RBA 10yr - 3dWindow Change"].cumsum()
data["RBA 10yr - 3dWindow Change Cumulative"] = data["RBA 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y Australian bond yield", color="dimgrey")
plt.plot(data.index, data["RBA 10yr - 3dWindow Change Cumulative"], label="10y Australian bond yield change around the RBA meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y Australian bond yield change around the Fed meetings", color="red")
plt.title("3-day windows around the RBA and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'two_bank_figs' / '2008_australian_bonds_figure1a.png')
plt.show()