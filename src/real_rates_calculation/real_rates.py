import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

# =============================================================================
# 1. Germany
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'german_govt_bond_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'german_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['real_interest_rate'] = ((1 + merged_data['10y Yield']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'german_real_rates.csv', index=False)

# =============================================================================
# 2. United Kingdom
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_spot_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'uk_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields = yields.reset_index()
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['real_interest_rate'] = ((1 + merged_data['10yr']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_real_rates.csv', index=False)

# =============================================================================
# 3. Japan
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'japanese_spot_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'japan_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields = yields.reset_index()
yields['Date'] = pd.to_datetime(yields['Date'], dayfirst=True)
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['real_interest_rate'] = ((1 + merged_data['10yr']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'japan_real_rates.csv', index=False)

#! There is a problem with this
# =============================================================================
# 4. Canada
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'canadian_spot_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'canada_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields = yields.reset_index()
yields['Date'] = pd.to_datetime(yields['Date'])
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['10.0yr'] = merged_data['10.0yr'].replace('na', np.nan)
merged_data['real_interest_rate'] = ((1 + merged_data['10.0yr']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'canada_real_rates.csv', index=False)

# =============================================================================
# 5. Switzerland
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'swiss_spot_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'swiss_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields = yields.reset_index()
yields['Date'] = pd.to_datetime(yields['Date'])
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['real_interest_rate'] = ((1 + merged_data['10yr']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'switzerland_real_rates.csv', index=False)

# =============================================================================
# 6. Australia
# =============================================================================
yields = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australian_spot_yields.pkl')
inf = pd.read_excel(PROJECT_DIR / 'original_data' / 'inflation_rates' / 'australia_inflation_yoy.xlsx')
inf['year'] = pd.to_datetime(inf['year'], format='%Y')
yields = yields.reset_index()
yields['Date'] = pd.to_datetime(yields['Date'])
yields['year'] = yields['Date'].dt.year
yields['year'] = pd.to_datetime(yields['year'], format='%Y')
merged_data = pd.merge(yields, inf, on='year', how='inner')
merged_data['real_interest_rate'] = ((1 + merged_data['10yr - AG']/100) / (1 + merged_data['inflation']/100) - 1)*100
merged_data.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'australia_real_rates.csv', index=False)

