import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

# ====================================================
# Germany
# ====================================================
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_german_spot_yields.csv')
usdeur = pd.read_csv(PROJECT_DIR / 'processed_data' / 'exchange_rates' / 'usdeur_with_spread.csv')

# Convert "Date" columns to datetime objects
data["Date"] = pd.to_datetime(data["Date"])
usdeur["Date"] = pd.to_datetime(usdeur["Date"])

# Merge the DataFrames on the "Date" column using a left join
merged_eur = pd.merge(data, usdeur, on="Date", how="left")

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
merged_cad = pd.merge(data, usdcad, on="Date", how="left")

# To export data
merged_cad.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'canada_master.csv', index=False)
merged_cad.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'canada_master.pkl')

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

# To export data
merged_aud.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'australia_master.csv', index=False)
merged_aud.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'australia_master.pkl')