import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'france_govt_bond_yields.pkl')

column_names = ["ECB MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/ecb_mpd.csv", header=None, names=column_names)
mpdd["ECB MP Dates"] = pd.to_datetime(mpdd["ECB MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

fed_yields = pd.read_excel(PROJECT_DIR / "original_data" / "gurkaynak2007.xlsx", sheet_name="Yields", index_col=0)
fed_yields.rename(columns={"SVENY10": "US10yr"}, inplace=True)
fed_yields.index = pd.to_datetime(fed_yields.index)

data.rename(columns={"1y Yield" : "1yr",
                    "2y Yield"  : "2yr",
                    "5y Yield"  : "5yr",
                    "10y Yield" : "10yr",
                    "20y Yield" : "20yr",
                    "30y Yield" : "30yr"}, 
                    inplace=True)

data.set_index('Date', inplace=True)
#data = data.loc[data.index >= '1997-06-01']
#data = data.loc[data.index >= '1999-01-01']
data = data.loc[data.index >= '2008-01-01']

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

# Calculate the "10yr" change for each date in the `data` DataFrame.
data["10yr Change"] = data["10yr"].diff()
data['US10yr'] = fed_yields['US10yr']
data['US10yr Change'] = data['US10yr'].diff()

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

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_french_spot_yields.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_french_spot_yields.pkl')

# ===============================================================================
# Plot 10y British Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["10yr Change Cumulative"] = data["10yr"].diff().cumsum()
data["ECB 10yr - 3dWindow Change Cumulative"] = data["ECB 10yr - 3dWindow Change"].cumsum()
data["ECB 10yr - 3dWindow Change Cumulative"] = data["ECB 10yr - 3dWindow Change Cumulative"].ffill()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change"].cumsum()
data["Fed 10yr - 3dWindow Change Cumulative"] = data["Fed 10yr - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["10yr Change Cumulative"], label="10y French OAT yield", color="dimgrey")
plt.plot(data.index, data["ECB 10yr - 3dWindow Change Cumulative"], label="10y French OAT yield change around the ECB meetings", color="blue")
plt.plot(data.index, data["Fed 10yr - 3dWindow Change Cumulative"], label="10y French OAT yield change around the Fed meetings", color="red")
plt.title("Cumulative Yield Change in French OATs", fontsize=16)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left', fontsize=12)
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_figures' / '1997_french_oats_figure1a.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_figures' / '1999_french_oats_figure1a.png')
plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_figures' / '2008_french_oats_figure1a.png')
plt.show()