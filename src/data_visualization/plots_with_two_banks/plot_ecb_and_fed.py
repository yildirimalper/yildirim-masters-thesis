import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'ecb_spot_yields.pkl')

column_names = ["ECB MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/ecb_mpd.csv", header=None, names=column_names)
mpdd["ECB MP Dates"] = pd.to_datetime(mpdd["ECB MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

# Convert the index to datetime and filter the data first
data.index = pd.to_datetime(data.index)
#data = data.loc[data.index >= '2008-01-01']

# For ECB
mpdd["ECB 3dWindow"] = mpdd["ECB MP Dates"].apply(create_3d_window)
mpdd["ECB 5dWindow"] = mpdd["ECB MP Dates"].apply(create_5d_window)
mpdd["ECB 7dWindow"] = mpdd["ECB MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
ecb_three_day_windows = pd.Series([date for sublist in mpdd["ECB 3dWindow"] for date in sublist])
ecb_five_day_windows = pd.Series([date for sublist in mpdd["ECB 5dWindow"] for date in sublist])
ecb_seven_day_windows = pd.Series([date for sublist in mpdd["ECB 7dWindow"] for date in sublist])

# For Fed
fed_mpdd["Fed 3dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_3d_window)
fed_mpdd["Fed 5dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_5d_window)
fed_mpdd["Fed 7dWindow"] = fed_mpdd["Fed MP Dates"].apply(create_7d_window)

# Flatten these columns into Series of dates that are within any three-day, five-day or seven-day window.
fed_three_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 3dWindow"] for date in sublist])
fed_five_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 5dWindow"] for date in sublist])
fed_seven_day_windows = pd.Series([date for sublist in fed_mpdd["Fed 7dWindow"] for date in sublist])

# Create new columns in the `data` DataFrame that indicates whether each date is within a three-day, five-day, or seven-day window.
data["In ECB 3dWindow"] = data.index.isin(ecb_three_day_windows)
data["In ECB 5dWindow"] = data.index.isin(ecb_five_day_windows)
data["In ECB 7dWindow"] = data.index.isin(ecb_seven_day_windows)

data["In Fed 3dWindow"] = data.index.isin(fed_three_day_windows)
data["In Fed 5dWindow"] = data.index.isin(fed_five_day_windows)
data["In Fed 7dWindow"] = data.index.isin(fed_seven_day_windows)

data.rename(columns={"10.0yr" : "10yr"}, inplace=True)

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()

# For ECB
data["ECB 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In ECB 3dWindow"], 0)
data["ECB 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In ECB 5dWindow"], 0)
data["ECB 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In ECB 7dWindow"], 0)

data["ECB 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In ECB 3dWindow"], 0)
data["ECB 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In ECB 5dWindow"], 0)
data["ECB 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In ECB 7dWindow"], 0)

# For Fed
data["Fed 10yr - 3dWindow Change"] = data["10yr Change"].where(data["In Fed 3dWindow"], 0)
data["Fed 10yr - 5dWindow Change"] = data["10yr Change"].where(data["In Fed 5dWindow"], 0)
data["Fed 10yr - 7dWindow Change"] = data["10yr Change"].where(data["In Fed 7dWindow"], 0)

data["Fed 10yr - Outside 3dWindow Change"] = data["10yr Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed 10yr - Outside 5dWindow Change"] = data["10yr Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed 10yr - Outside 7dWindow Change"] = data["10yr Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_ecb_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_ecb_spot_yields.pkl')

# ===============================================================================
# Plot 10y British Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["ECB 10yr - 3dWindow Change Cumulative"] = data["ECB 10yr - 3dWindow Change"].cumsum()
data["ECB 10yr - 3dWindow Change Cumulative"] = data["ECB 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y AAA-rated European bond yield", color="dimgrey")
plt.plot(data.index, data["ECB 10yr - 3dWindow Change Cumulative"], label="10y AAA-rated European yield change around the ECB meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y AAA-rated European yield change around the Fed meetings", color="red")
# the EU QEs
plt.axvspan('2010-05-10', '2011-03-25', color='grey', alpha=0.3, label="ECB's Securities Markets Programme")
plt.axvspan('2011-08-08', '2012-09-06', color='grey', alpha=0.3)
# the US QEs
plt.axvspan('2008-11-25', '2010-03-31', color='wheat', alpha=0.3, label="Quantitative Easing by the Fed")
plt.axvspan('2010-11-03', '2011-06-30', color='wheat', alpha=0.3)
plt.axvspan('2012-09-13', '2014-10-29', color='wheat', alpha=0.3)
plt.title("3-day windows around the ECB and Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figures' / 'two_bank_figures' / 'european_bonds_2008_figure1a.png')
plt.show()