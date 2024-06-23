import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scienceplots

plt.style.use('science')

PROJECT_DIR = Path().resolve()

# Load data
data = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_spot_yields.csv')

# Convert Date to datetime and set as index
data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
#data.drop(columns={'Unnamed: 0'}, inplace=True) # for SNB
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y') # for Ecb
data.set_index('Date', inplace=True)
data = data.iloc[:, ::-1]
data.columns = data.columns.str.replace('yr', '', regex=True)

# data = data.replace(r".*na.*", np.nan, regex=True) #for Canada
# data = data.replace(' ', np.nan)
# data = data.dropna() # again for Canada
# data = data.dropna(thresh=len(data) - 2200, axis=1) #for UK
# data = data.dropna() #for UK
# for Japan
# data = data.drop(["15", "25", "30", "40"], axis=1)
# data.columns = data.columns.str.replace('yr', '', regex=True)
# data = data.apply(pd.to_numeric, errors='coerce')
# data.index = pd.to_datetime(data.index, format='%d/%m/%Y')


# Create high resolution 3D plot
fig = plt.figure(figsize=(10, 6), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# Convert dates to number of days since first date
X_numeric = (data.index - data.index[0]).days
#X_years = data.index.year
X_years = data.index.year.dropna().astype(int)
maturities = pd.to_numeric(data.columns)

# Create 2D arrays for X, Y, and Z
X, Y = np.meshgrid(X_numeric, maturities)
Z = data.T.values  # Transpose DataFrame before extracting values

# Plot surface
ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none', rstride=10, cstride=10)

# Set x-ticks and x-ticklabels to display years
ax.set_xticks(X_numeric[::1400])  # Change 288 to a different number if you want more or less ticks
ax.set_xticklabels(X_years[::1400])  # Change 288 to a different number if you want more or less ticks

ax.set_xlabel('Year')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield (\%)')

# Save figure
plt.savefig('figs/yield_curves/boe_yield_curve.png', format='png', dpi=300)

plt.show()