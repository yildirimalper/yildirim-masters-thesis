import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns
from utils.time_windows import create_3d_window, create_5d_window, create_7d_window

PROJECT_DIR = Path().resolve()
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'german_real_rates.csv')

column_names = ["ECB MP Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_dates/ecb_mpd.csv", header=None, names=column_names)
mpdd["ECB MP Dates"] = pd.to_datetime(mpdd["ECB MP Dates"])

column_names = ["Fed MP Dates"]
fed_mpdd = pd.read_csv("processed_data/monetary_policy_dates/fed_mpd.csv", header=None, names=column_names)
fed_mpdd["Fed MP Dates"] = pd.to_datetime(fed_mpdd["Fed MP Dates"])

data.rename(columns={"1y Yield" : "1yr",
                    "2y Yield"  : "2yr",
                    "5y Yield"  : "5yr",
                    "10y Yield" : "10yr",
                    "20y Yield" : "20yr",
                    "30y Yield" : "30yr"}, 
                    inplace=True)

data["Date"] = pd.to_datetime(data["Date"])
data.set_index('Date', inplace=True)
#data = data.loc[data.index >= '1997-06-01']
data = data.loc[data.index >= '1999-01-01']
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

# Calculate the "real_interest_rate" change for each date in the `data` DataFrame.
data["real_interest_rate Change"] = data["real_interest_rate"].diff()

# For ECB
data["ECB real_interest_rate - 3dWindow Change"] = data["real_interest_rate Change"].where(data["In ECB 3dWindow"], 0)
data["ECB real_interest_rate - 5dWindow Change"] = data["real_interest_rate Change"].where(data["In ECB 5dWindow"], 0)
data["ECB real_interest_rate - 7dWindow Change"] = data["real_interest_rate Change"].where(data["In ECB 7dWindow"], 0)

data["ECB real_interest_rate - Outside 3dWindow Change"] = data["real_interest_rate Change"].where(~data["In ECB 3dWindow"], 0)
data["ECB real_interest_rate - Outside 5dWindow Change"] = data["real_interest_rate Change"].where(~data["In ECB 5dWindow"], 0)
data["ECB real_interest_rate - Outside 7dWindow Change"] = data["real_interest_rate Change"].where(~data["In ECB 7dWindow"], 0)

# For Fed
data["Fed real_interest_rate - 3dWindow Change"] = data["real_interest_rate Change"].where(data["In Fed 3dWindow"], 0)
data["Fed real_interest_rate - 5dWindow Change"] = data["real_interest_rate Change"].where(data["In Fed 5dWindow"], 0)
data["Fed real_interest_rate - 7dWindow Change"] = data["real_interest_rate Change"].where(data["In Fed 7dWindow"], 0)

data["Fed real_interest_rate - Outside 3dWindow Change"] = data["real_interest_rate Change"].where(~data["In Fed 3dWindow"], 0)
data["Fed real_interest_rate - Outside 5dWindow Change"] = data["real_interest_rate Change"].where(~data["In Fed 5dWindow"], 0)
data["Fed real_interest_rate - Outside 7dWindow Change"] = data["real_interest_rate Change"].where(~data["In Fed 7dWindow"], 0)

data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'deneme.csv')
data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_german_spot_yields.pkl')

# ===============================================================================
# Plot 10y British Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
data["real_interest_rate Change Cumulative"] = data["real_interest_rate"].diff().cumsum()
data["ECB real_interest_rate - 3dWindow Change Cumulative"] = data["ECB real_interest_rate - 3dWindow Change"].cumsum()
data["ECB real_interest_rate - 3dWindow Change Cumulative"] = data["ECB real_interest_rate - 3dWindow Change Cumulative"].ffill()
data["Fed real_interest_rate - 3dWindow Change Cumulative"] = data["Fed real_interest_rate - 3dWindow Change"].cumsum()
data["Fed real_interest_rate - 3dWindow Change Cumulative"] = data["Fed real_interest_rate - 3dWindow Change Cumulative"].ffill()

plt.figure(figsize=(10, 6))
plt.plot(data.index, data["real_interest_rate Change Cumulative"], label="10y German bund yield", color="dimgrey")
plt.plot(data.index, data["ECB real_interest_rate - 3dWindow Change Cumulative"], label="10y German bund yield change around the ECB meetings", color="blue")
plt.plot(data.index, data["Fed real_interest_rate - 3dWindow Change Cumulative"], label="10y German bund yield change around the Fed meetings", color="red")
plt.title("Cumulative Yield Change in German Bunds", fontsize=16)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left', fontsize=12)
plt.tight_layout()
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_real_rates' / '1997_german_bunds_figure1a.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_real_rates' / '1999_german_bunds_figure1a.png')
#plt.savefig(PROJECT_DIR / 'figs' / 'two_bank_real_rates' / '2008_german_bunds_figure1a.png')
plt.show()