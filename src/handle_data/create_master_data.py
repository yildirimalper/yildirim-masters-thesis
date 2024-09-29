import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

vix = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'vix.xlsx')
dxy = pd.read_csv(PROJECT_DIR / 'processed_data' / 'control_variables' / 'dxy.csv')
vix['date'] = pd.to_datetime(vix['date'])
dxy['date'] = pd.to_datetime(dxy['date'])

# ====================================================
# Germany
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_german_spot_yields.csv')
usdeur = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdeur_with_spread.csv')
gdp = pd.read_csv(PROJECT_DIR / 'processed_data' / 'control_variables' / 'gdp_per_cap.csv')
gdp.rename(columns={"date": "Date"}, inplace=True)
igrea = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'igrea.xls')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdeur["Date"] = pd.to_datetime(usdeur["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_eur = pd.merge(data, usdeur, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_ger = gdp[gdp["country"] == "DEU"]
gdp_ger["Date"] = pd.to_datetime(gdp_ger["Date"])
merged_eur = pd.merge(merged_eur, gdp_ger, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_eur[columns_to_fill] = merged_eur[columns_to_fill].ffill()
merged_eur[columns_to_fill] = merged_eur[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_eur["country"] = "DEU"

merged_eur = merged_eur.merge(vix, how='left', left_on='Date', right_on='date')
merged_eur = merged_eur.merge(dxy, how='left', left_on='Date', right_on='date')
merged_eur = merged_eur.drop(columns=['date_x', 'date_y'])
merged_eur["In Fed 3dWindow"] = merged_eur["In Fed 3dWindow"].astype(int)
merged_eur["Spread"] = merged_eur["Spread"] * 100

# To export data
merged_eur.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'german_master.csv', index=False)
merged_eur.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'german_master.pkl')

# ====================================================
# United Kingdom
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_uk_spot_yields.csv')
usdgbp = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdgbp_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdgbp["Date"] = pd.to_datetime(usdgbp["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_gbp = pd.merge(data, usdgbp, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_gbp = gdp[gdp["country"] == "GBP"]
gdp_gbp["Date"] = pd.to_datetime(gdp_gbp["Date"])
merged_gbp = pd.merge(merged_gbp, gdp_gbp, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_gbp[columns_to_fill] = merged_gbp[columns_to_fill].ffill()
merged_gbp[columns_to_fill] = merged_gbp[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_gbp["country"] = "GBP"

merged_gbp = merged_gbp.merge(vix, how='left', left_on='Date', right_on='date')
merged_gbp = merged_gbp.merge(dxy, how='left', left_on='Date', right_on='date')
merged_gbp = merged_gbp.drop(columns=['date_x', 'date_y'])
merged_gbp["In Fed 3dWindow"] = merged_gbp["In Fed 3dWindow"].astype(int)
merged_gbp["Spread"] = merged_gbp["Spread"] * 100

# To export data
merged_gbp.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'uk_master.csv', index=False)
merged_gbp.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'uk_master.pkl')

# ====================================================
# Japan
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_japan_spot_yields.csv')
usdjpy = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdjpy_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdjpy["Date"] = pd.to_datetime(usdjpy["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_jpy = pd.merge(data, usdjpy, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_jpy = gdp[gdp["country"] == "JPY"]
gdp_jpy["Date"] = pd.to_datetime(gdp_jpy["Date"])
merged_jpy = pd.merge(merged_jpy, gdp_jpy, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_jpy[columns_to_fill] = merged_jpy[columns_to_fill].ffill()
merged_jpy[columns_to_fill] = merged_jpy[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_jpy["country"] = "JPY"

merged_jpy = merged_jpy.merge(vix, how='left', left_on='Date', right_on='date')
merged_jpy = merged_jpy.merge(dxy, how='left', left_on='Date', right_on='date')
merged_jpy = merged_jpy.drop(columns=['date_x', 'date_y'])
merged_jpy["In Fed 3dWindow"] = merged_jpy["In Fed 3dWindow"].astype(int)
merged_jpy["Spread"] = merged_jpy["Spread"] * 100

# To export data
merged_jpy.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'japan_master.csv', index=False)
merged_jpy.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'japan_master.pkl')

# ====================================================
# Canada
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_canada_spot_yields.csv')
usdcad = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdcad_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdcad["Date"] = pd.to_datetime(usdcad["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_can = pd.merge(data, usdcad, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_can = gdp[gdp["country"] == "CAN"]
gdp_can["Date"] = pd.to_datetime(gdp_can["Date"])
merged_can = pd.merge(merged_can, gdp_can, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_can[columns_to_fill] = merged_can[columns_to_fill].ffill()
merged_can[columns_to_fill] = merged_can[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_can["country"] = "CAN"

merged_can = merged_can.merge(vix, how='left', left_on='Date', right_on='date')
merged_can = merged_can.merge(dxy, how='left', left_on='Date', right_on='date')
merged_can = merged_can.drop(columns=['date_x', 'date_y'])
merged_can["In Fed 3dWindow"] = merged_can["In Fed 3dWindow"].astype(int)
merged_can["Spread"] = merged_can["Spread"] * 100

# To export data
merged_can.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'canada_master.csv', index=False)
merged_can.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'canada_master.pkl')

# ====================================================
# Switzerland
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_swiss_spot_yields.csv')
usdchf = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdchf_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdchf["Date"] = pd.to_datetime(usdchf["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_chf = pd.merge(data, usdchf, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_chf = gdp[gdp["country"] == "CHE"]
gdp_chf["Date"] = pd.to_datetime(gdp_chf["Date"])
merged_chf = pd.merge(merged_chf, gdp_chf, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_chf[columns_to_fill] = merged_chf[columns_to_fill].ffill()
merged_chf[columns_to_fill] = merged_chf[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_chf["country"] = "CHE"

merged_chf = merged_chf.merge(vix, how='left', left_on='Date', right_on='date')
merged_chf = merged_chf.merge(dxy, how='left', left_on='Date', right_on='date')
merged_chf = merged_chf.drop(columns=['date_x', 'date_y'])
merged_chf["In Fed 3dWindow"] = merged_chf["In Fed 3dWindow"].astype(int)
merged_chf["Spread"] = merged_chf["Spread"] * 100

# To export data
merged_chf.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'switzerland_master.csv', index=False)
merged_chf.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'switzerland_master.pkl')

# ====================================================
# Australia
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_australia_spot_yields.csv')
usdaud = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdaud_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdaud["Date"] = pd.to_datetime(usdaud["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_aud = pd.merge(data, usdaud, on="Date", how="left")

# Merge the filtered GDP data with merged_eur on the "Date" column using a left join
gdp_aud = gdp[gdp["country"] == "AUS"]
gdp_aud["Date"] = pd.to_datetime(gdp_aud["Date"])
merged_aud = pd.merge(merged_aud, gdp_aud, on="Date", how="left")

# Columns to forward fill and backward fill
columns_to_fill = [
    "gdp_per_cap",
    "log_gpc",
    "qrtly_chng_gpc",
    "yearly_chng_gpc",
    "log_qrtly_chng_gpc",
    "log_yearly_chng_gpc"
]
# Forward fill the specified columns
merged_aud[columns_to_fill] = merged_aud[columns_to_fill].ffill()
merged_aud[columns_to_fill] = merged_aud[columns_to_fill].bfill()

# Fill missing values in the "country" column with "GBP"
merged_aud["country"] = "AUS"

merged_aud = merged_aud.merge(vix, how='left', left_on='Date', right_on='date')
merged_aud = merged_aud.merge(dxy, how='left', left_on='Date', right_on='date')
merged_aud = merged_aud.drop(columns=['date_x', 'date_y'])
merged_aud["In Fed 3dWindow"] = merged_aud["In Fed 3dWindow"].astype(int)
merged_aud["Spread"] = merged_aud["Spread"] * 100

# To export data
merged_aud.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'australia_master.csv', index=False)
merged_aud.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'australia_master.pkl')

# ====================================================
# Concatenate all the data
# ====================================================

# Concatenate all the data
data = pd.concat([merged_eur, merged_gbp, merged_jpy, merged_can, merged_chf, merged_aud], ignore_index=True)

# To export data
data.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_data.csv', index=False)
data.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_data.pkl')