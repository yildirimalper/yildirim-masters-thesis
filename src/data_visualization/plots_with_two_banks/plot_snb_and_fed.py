import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'swiss_spot_yields.pkl')

column_names = ["SNB MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/snb_mpd.csv", header=None, names=column_names)
mpdd["SNB MP Dates"] = pd.to_datetime(mpdd["SNB MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Convert the index to datetime and filter the data first
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
#data = data.loc[data.index >= '2000-01-01']
data = data.loc[data.index >= '2008-01-01']

# For SNB
mpdd["SNB 3dWindow"] = mpdd["SNB MP Dates"].apply(create_3d_window)
mpdd["SNB 5dWindow"] = mpdd["SNB MP Dates"].apply(create_5d_window)
mpdd["SNB 7dWindow"] = mpdd["SNB MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
snb_three_day_windows = pd.Series([date for sublist in mpdd["SNB 3dWindow"] for date in sublist])
snb_five_day_windows = pd.Series([date for sublist in mpdd["SNB 5dWindow"] for date in sublist])
snb_seven_day_windows = pd.Series([date for sublist in mpdd["SNB 7dWindow"] for date in sublist])

# For Fed
fed_mpdd["Fed 3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["Fed 5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["Fed 7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 7dWindow"] for date in sublist])

# Create new columns in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In SNB 3dWindow"] = data.index.isin(snb_three_day_windows)
data["In SNB 5dWindow"] = data.index.isin(snb_five_day_windows)
data["In SNB 7dWindow"] = data.index.isin(snb_seven_day_windows)

data["In Fed 3dWindow"] = data.index.isin(fed_three_day_windows)
data["In Fed 5dWindow"] = data.index.isin(fed_five_day_windows)
data["In Fed 7dWindow"] = data.index.isin(fed_seven_day_windows)

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

# For SNB
data["SNB 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In SNB 3dWindow"], 0)
data["SNB 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In SNB 5dWindow"], 0)
data["SNB 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In SNB 7dWindow"], 0)

data["SNB 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In SNB 3dWindow"], 0)
data["SNB 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In SNB 5dWindow"], 0)
data["SNB 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In SNB 7dWindow"], 0)

# For Fed
data["Fed 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In Fed 3dWindow"], 0)
data["Fed 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In Fed 5dWindow"], 0)
data["Fed 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In Fed 7dWindow"], 0)

data["Fed 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_swiss_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_swiss_spot_yields.pkl')

# ===============================================================================
# Plot 10y Swiss Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["SNB 10yr - 3dWindow Change Cumulative"] = data["SNB 10yr - 3dWindow Change"].cumsum()
data["SNB 10yr - 3dWindow Change Cumulative"] = data["SNB 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y UK gilt yield", color="dimgrey")
plt.plot(data.index, data["SNB 10yr - 3dWindow Change Cumulative"], label="10y Swiss bond yield change around the SNB meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y Swiss bond yield change around the Fed meetings", color="red")
plt.title("Cumulative Yield Change in Swiss Confederation Bonds", fontsize=16)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left', fontsize=12)
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_figures' / '2000_swiss_bonds_figure1a.png')
plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_figures' / '2008_swiss_bonds_figure1a.png')
plt.show()