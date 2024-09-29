import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

data = pd.read_csv(PROJECT_DIR / "original_data" / 'gdppercap.csv')

# Function to convert "YYYY-Qn" to datetime
def convert_quarter_to_date(quarter_str):
    year, quarter = quarter_str.split('-Q')
    month = (int(quarter) - 1) * 3 + 1
    return pd.Timestamp(year=int(year), month=month, day=1)

# Convert "TIME_PERIOD" column to datetime object
data['TIME_PERIOD'] = data['TIME_PERIOD'].apply(convert_quarter_to_date)
data = data[data['TIME_PERIOD'] > '1990-01-01']

# Subset data where PRICE_BASE is "LR"
data = data[data['PRICE_BASE'] == 'LR']

# Filter data for specific countries
countries = ['USA', 'DEU', 'GBR', 'JPN', 'CAN', 'CHE', 'AUS']
data = data[data['REF_AREA'].isin(countries)]

data.rename(columns={   'TIME_PERIOD': 'date',
                        'REF_AREA': 'country', 
                        'OBS_VALUE': 'gdp_per_cap'}, 
                        inplace=True)

# Drop all other columns except 'date', 'country', and 'gdp_per_cap'
data = data[['date', 'country', 'gdp_per_cap']]

# Ensure data is grouped by country and sorted by date
data = data.sort_values(by=['country', 'date'])

# Create log GDP per capita variable
data['log_gpc'] = np.log(data['gdp_per_cap'])

# Create quarterly change in GDP per capita variable
data['qrtly_chng_gpc'] = data.groupby('country')['gdp_per_cap'].diff()

# Create change in GDP per capita with respect to the same quarter last year variable
data['yearly_chng_gpc'] = data.groupby('country')['gdp_per_cap'].diff(4)

# Replace zero or negative values with NaN before taking the logarithm
data['qrtly_chng_gpc'] = data['qrtly_chng_gpc'].replace(0, np.nan)
data['yearly_chng_gpc'] = data['yearly_chng_gpc'].replace(0, np.nan)

# Create log versions of the quarterly and yearly change variables
data['log_qrtly_chng_gpc'] = np.log(data['qrtly_chng_gpc'])
data['log_yearly_chng_gpc'] = np.log(data['yearly_chng_gpc'])

data.to_csv(PROJECT_DIR / 'processed_data' / 'control_variables' / 'gdp_per_cap.csv', index=False)