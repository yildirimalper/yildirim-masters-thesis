import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

dxy = pd.read_csv(PROJECT_DIR / 'original_data' /'dxy.csv')

# Drop irrelevant columns
dxy.drop(columns=["Open", "High", "Low", "Close", "Volume"],
        inplace=True)

# Rename for the future operations
dxy.rename(columns={"Adj Close": "dxy", "Date": "date"},
        inplace=True)

# In order to drop NaN values
dxy.replace("null", np.nan, inplace=True)

dxy['date'] = pd.to_datetime(dxy['date'], format='%d-%m-%Y')