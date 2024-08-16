import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
from linearmodels.iv import IV2SLS
import matplotlib.pyplot as plt
import seaborn as sns
from stargazer.stargazer import Stargazer
from stargazer.stargazer import Label

PROJECT_DIR = Path().resolve()

vix = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'vix.xlsx')
dxy = pd.read_csv(PROJECT_DIR / 'processed_data' / 'control_variables' / 'dxy.csv')
vix['date'] = pd.to_datetime(vix['date'])
dxy['date'] = pd.to_datetime(dxy['date'])

# 1. Germany
germany = pd.read_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'german_master.csv')
germany['Date'] = pd.to_datetime(germany['Date'])
# Merge the dataframes and drop the redundant 'date' columns from vix and dxy
germany = germany.merge(vix, how='left', left_on='Date', right_on='date')
germany = germany.merge(dxy, how='left', left_on='Date', right_on='date')
germany = germany.drop(columns=['date_x', 'date_y'])
germany["In Fed 3dWindow"] = germany["In Fed 3dWindow"].astype(int)
germany["Spread"] = germany["Spread"] * 100
germany = germany.replace([np.inf, -np.inf], np.nan).dropna(subset=["10yr Change", "In Fed 3dWindow", "Spread", "Interaction", "dxy","vix"])
#! Ara çıkış
germany.to_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'german_master.csv', index=False)