import pandas as pd
from pathlib import Path

PROJECT_DIR = Path().resolve()

data = pd.read_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'igrea.xls')

# Ensure 'date' is of datetime type
data['date'] = pd.to_datetime(data['date'])

# Set 'date' as the index
data.set_index('date', inplace=True)

# Resample to daily level and forward fill missing values
data_daily = data.resample('D').ffill()

# Export and overwrite the original file
data_daily.to_excel(PROJECT_DIR / 'processed_data' / 'control_variables' / 'igrea.xls')