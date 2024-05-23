import pandas as pd
import numpy as np 
from pathlib import Path

PROJECT_DIR = Path().resolve()

dxy = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'control_variables' / 'dxy.pkl')
dxy['date'] = pd.to_datetime(dxy['date'])
igrea = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'igrea.xls')
igrea['date'] = pd.to_datetime(igrea['date'])
vix = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'vix.xlsx')
vix['date'] = pd.to_datetime(vix['date'])

# ===============================================================================
# 1. European Central Bank
# ===============================================================================
ecb = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_ecb_spot_yields.csv')
ecb.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
ecb['date']   = pd.to_datetime(ecb['date'])
merged_ecb = ecb.merge(dxy, how='left', on='date')
merged_ecb['date'] = pd.to_datetime(merged_ecb['date'])
merged_ecb_2 = merged_ecb.merge(vix, how='left', on='date')
merged_ecb_2['date'] = pd.to_datetime(merged_ecb_2['date'])
merged_ecb_3 = merged_ecb_2.merge(igrea, how='left', on='date')
merged_ecb_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_ecb.pkl')

# ===============================================================================
# 2. Bank of England
# ===============================================================================
boe = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_uk_spot_yields.pkl')
boe.reset_index(inplace=True)
boe.rename(columns={'Date' : 'date'}, inplace=True)
boe['date'] = pd.to_datetime(boe['date'])
merged_boe = boe.merge(dxy, how='left', on='date')
merged_boe['date'] = pd.to_datetime(merged_boe['date'])
merged_boe_2 = merged_boe.merge(vix, how='left', on='date')
merged_boe_2['date'] = pd.to_datetime(merged_boe_2['date'])
merged_boe_3 = merged_boe_2.merge(igrea, how='left', on='date')
merged_boe_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_boe.pkl')

# ===============================================================================
# 3. Bank of Japan
# ===============================================================================
boj = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_japanese_spot_yields.pkl')
boj.reset_index(inplace=True)
boj.rename(columns={'Date' : 'date'}, inplace=True)
boj['date'] = pd.to_datetime(boj['date'])
merged_boj = boj.merge(dxy, how='left', on='date')
merged_boj['date'] = pd.to_datetime(merged_boj['date'])
merged_boj_2 = merged_boj.merge(vix, how='left', on='date')
merged_boj_2['date'] = pd.to_datetime(merged_boj_2['date'])
merged_boj_3 = merged_boj_2.merge(igrea, how='left', on='date')
merged_boj_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_boj.pkl')

# ===============================================================================
# 4. Swiss National Bank
# ===============================================================================
snb = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_swiss_spot_yields.pkl')
snb.reset_index(inplace=True)
snb.rename(columns={'Date' : 'date'}, inplace=True)
snb['date'] = pd.to_datetime(snb['date'])
merged_snb = snb.merge(dxy, how='left', on='date')
merged_snb['date'] = pd.to_datetime(merged_snb['date'])
merged_snb_2 = merged_snb.merge(vix, how='left', on='date')
merged_snb_2['date'] = pd.to_datetime(merged_snb_2['date'])
merged_snb_3 = merged_snb_2.merge(igrea, how='left', on='date')
merged_snb_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_snb.pkl')

# ===============================================================================
# 5. Reserve Bank of Australia
# ===============================================================================
rba = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_australian_spot_yields.pkl')
rba.reset_index(inplace=True)
rba.rename(columns={'Date' : 'date'}, inplace=True)
rba['date'] = pd.to_datetime(rba['date'])
merged_rba = rba.merge(dxy, how='left', on='date')
merged_rba['date'] = pd.to_datetime(merged_rba['date'])
merged_rba_2 = merged_rba.merge(vix, how='left', on='date')
merged_rba_2['date'] = pd.to_datetime(merged_rba_2['date'])
merged_rba_3 = merged_rba_2.merge(igrea, how='left', on='date')
merged_rba_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_rba.pkl')

# ===============================================================================
# 6. Bank of Canada
# ===============================================================================
boc = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_canadian_spot_yields.pkl')
boc.reset_index(inplace=True)
boc.rename(columns={'Date' : 'date'}, inplace=True)
boc['date'] = pd.to_datetime(boc['date'])
merged_boc = boc.merge(dxy, how='left', on='date')
merged_boc['date'] = pd.to_datetime(merged_boc['date'])
merged_boc_2 = merged_boc.merge(vix, how='left', on='date')
merged_boc_2['date'] = pd.to_datetime(merged_boc_2['date'])
merged_boc_3 = merged_boc_2.merge(igrea, how='left', on='date')
merged_boc_3.to_pickle(PROJECT_DIR / 'processed_data' / 'master_data' / 'master_boc.pkl')
