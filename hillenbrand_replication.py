import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns

# Initial Setup
PROJECT_DIR = Path().resolve()
data = pd.read_excel(PROJECT_DIR / "original_data" / "gurkaynak2007.xlsx", sheet_name="Yields", index_col=0)

data.index = pd.to_datetime(data.index)
cutoff_date = pd.to_datetime('1989-06-01')
data = data[data.index >= cutoff_date]
data = data.sort_index()

# Import FOMC meeting dates
column_names = ["MP Dates"]
mpdd = pd.read_csv("processed_data/fomc_meeting_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])

def create_3d_window(date):
    """
    Create a list of dates that are within a three-day window around a given date.
    """
    return pd.date_range(start=date - Day(1), end=date + Day(1))

# Apply this function to the "MP Dates" column of the `mpdd` DataFrame to create a new column "3dWindow" that contains lists of these three-day windows.
mpdd["3dWindow"] = mpdd["MP Dates"].apply(create_3d_window)
# Flatten this column into a Series of dates that are within any three-day window.
three_day_windows = pd.Series([date for sublist in mpdd["3dWindow"] for date in sublist])
# Create a new column in the `data` DataFrame that indicates whether each date is within a three-day window.
data["In 3dWindow"] = data.index.isin(three_day_windows)
# Calculate the "SVENY10" change for each date in the `data` DataFrame.
data["SVENY10 Change"] = data["SVENY10"].diff()
# Create a new column "SVENY10 - 3dWindow Change" in the `data` DataFrame that contains the "SVENY10" change if the date is within a three-day window, and 0 otherwise.
data["SVENY10 - 3dWindow Change"] = data["SVENY10 Change"].where(data["In 3dWindow"], 0)
# Create a new column "SVENY10 - Outside 3dWindow Change" in the `data` DataFrame that contains the "SVENY10" change if the date is outside a three-day window, and 0 otherwise.
data["SVENY10 - Outside 3dWindow Change"] = data["SVENY10 Change"].where(~data["In 3dWindow"], 0)

# ===============================================================================
# Plot 10y Treasury Cumulative Yield Change (Hillenbrand, Figure 1, Panel A)
# ===============================================================================
# Calculate the day-by-day changes and the cumulative sum of these changes
data["SVENY10 Change Cumulative"] = data["SVENY10"].diff().cumsum()
data["SVENY10 - 3dWindow Change Cumulative"] = data["SVENY10 - 3dWindow Change"].cumsum()
data["SVENY10 - 3dWindow Change Cumulative"] = data["SVENY10 - 3dWindow Change Cumulative"].ffill()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["SVENY10 Change Cumulative"], label="10y Treasury yield", color="dimgrey")
plt.plot(data.index, data["SVENY10 - 3dWindow Change Cumulative"], label="10y Treasury yield change around the Fed meetings", color="red")
plt.title("3-day windows around the Fed meetings", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
#plt.xlim(datetime.datetime(1989, 6, 1), data.index.max())
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'hillenbrand_replication' / 'figure1_panelA.png')
plt.show()

# ===============================================================================
# Outside 3-day windows around the Fed meetings
# ===============================================================================
# Calculate the cumulative sum of these changes
data["SVENY10 - Outside 3dWindow Change Cumulative"] = data["SVENY10 - Outside 3dWindow Change"].cumsum()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data.index, data["SVENY10 Change Cumulative"], label="10y Treasury yield", color="dimgrey", alpha=0.9)
plt.plot(data.index, data["SVENY10 - Outside 3dWindow Change Cumulative"], label="10y Treasury yield change outside of fed window", color="silver", alpha=0.9)
plt.title("Days outside 3-day the Fed window", fontsize=14)
plt.ylabel("Cumulative Yield Change (%)", fontsize=12)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig(PROJECT_DIR / 'figures' / 'hillenbrand_replication' / 'figure1_panelB.png')
plt.show()

# ===============================================================================
# Export data for further checks
# ===============================================================================

data.to_csv(PROJECT_DIR / 'processed_data' / 'hillenbrand_replication.csv', index=True)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'hillenbrand_replication.pkl')