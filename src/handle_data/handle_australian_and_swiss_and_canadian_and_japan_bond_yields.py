import pandas as pd
import numpy as np
from pathlib import Path
import re

PROJECT_DIR = Path().resolve()

# ==============================================================
# Australian Bond Data
# ==============================================================
zc_data = pd.read_excel(PROJECT_DIR / 'original_data' / 'australian_bond_yields' / 'zcr-analytical-series-hist.xls',
                        sheet_name='Yields',
                        index_col=0)

reg_data = pd.read_excel(PROJECT_DIR / 'original_data' / 'australian_bond_yields' / 'f02dhist.xls',
                        sheet_name='Data',
                        index_col=0)

zc_data.columns = [f'{str(col)}yr' for col in zc_data.columns]

zc_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_zero_cpn_spot_yields.csv', index=True)
zc_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_zero_cpn_spot_yields.pkl')

reg_data.rename(columns={
    'AG_2 yrs'  : '2yr - AG',
    'AG_3 yrs'  : '3yr - AG',
    'AG_5 yrs'  : '5yr - AG',
    'AG_10 yrs' : '10yr - AG',
    'NSW_3 yrs' : '3yr - NSW',
    'NSW_5 yrs' : '5yr - NSW',
    'NSW_10 yrs': '10yr - NSW',
}, inplace=True)

reg_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_spot_yields.csv', index=True)
reg_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_spot_yields.pkl')

# ==============================================================
# Swiss Bond Data
# ==============================================================
snb_data = pd.read_excel(PROJECT_DIR / 'original_data' / 'swiss_bond_yields' / 'snb-chart-data-rendeidglfzch-en-all-20240402_1430.xlsx')

snb_data.rename(columns={
    '2 years' : '2yr',
    '5 years' : '5yr',
    '10 years' : '10yr',
    '20 years' : '20yr'
}, inplace=True)

snb_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'swiss_spot_yields.csv', index=True)
snb_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'swiss_spot_yields.pkl')

# ==============================================================
# Canadian Bond Data
# ==============================================================
boc_data = pd.read_csv(PROJECT_DIR / 'original_data' / 'boc_bond_yield' / 'yield_curves.csv', index_col=0)
# Python
for col in boc_data.columns:
    numeric_part = col.replace("ZC", "").replace("YR", "")
    numeric_part = int(numeric_part)
    numeric_part = numeric_part / 100
    new_col_name = f"{numeric_part}yr"
    boc_data.rename(columns={col: new_col_name}, inplace=True)

empty_row_indices = boc_data[boc_data.isnull().all(axis=1)].index

boc_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'canadian_spot_yields.csv', index=True)
boc_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'canadian_spot_yields.pkl')

# ==============================================================
# Japanese Bond Data
# ==============================================================

boj_data = pd.read_csv(PROJECT_DIR / 'original_data' / 'japanese_bond_yields' / 'jgbcme_all.csv', index_col=0)
boj_data.columns = [col.replace('Y', 'yr') for col in boj_data.columns]
boj_data.replace("-", np.nan, inplace=True)
boj_data = boj_data.astype('float64')
boj_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'japanese_spot_yields.csv', index=True)
boj_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'japanese_spot_yields.pkl')

# ==============================================================
# Some further arrangements on ECB, German and French Yields
# ==============================================================
ecb_data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'ecb_spot_yields.csv', index_col=0)
ecb_data.columns = [re.findall(r'\d+', col)[0] + 'yr' for col in ecb_data.columns]
ecb_forward_data = ecb_forward_data.drop(ecb_forward_data.columns[-1], axis=1)
ecb_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'ecb_spot_yields.csv', index=True)
ecb_data.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'ecb_spot_yields.pkl')