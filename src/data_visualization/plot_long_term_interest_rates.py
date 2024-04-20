import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from datetime import datetime
from matplotlib.dates import DateFormatter
import matplotlib.ticker as mtick
from pathlib import Path
import scienceplots

plt.style.use('science')

PROJECT_DIR = Path().resolve()

data = pd.read_csv(PROJECT_DIR / 'original_data' / 'long-term-interest-oecd.csv')

# Filter data
data = data[data['FREQUENCY'] == 'M']
data = data[data["Subject"] == "Long-term interest rates, Per cent per annum"]
countries = ["Australia", "Canada", "France", "Germany", "Japan", "United Kingdom", "United States"]
data = data[data['Country'].isin(countries)]

# Convert TIME to datetime and set as index
data['TIME'] = pd.to_datetime(data['TIME'])
data.set_index('TIME', inplace=True)

# Restrict observations to after 1980
data = data[data.index.year >= 1980]

# Sort data by index (date)
data.sort_index(inplace=True)

mpl.rcParams['xtick.labelsize'] = 13
mpl.rcParams['ytick.labelsize'] = 13
mpl.rcParams['axes.labelsize'] = 14

# Plot data
plt.figure(figsize=(10,6), dpi=300)
for country in countries:
    country_data = data[data['Country'] == country]
    plt.plot(country_data.index, country_data['Value'], label=country)

plt.ylabel('Long-Term Nominal Interest Rates')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.axhline(0, color='black', linewidth=0.5, alpha=0.5)  # Add horizontal line at zero
plt.legend(fontsize='large')
plt.tight_layout()
plt.savefig('figures/long-term-rates1.png', format='png', dpi=300)
plt.show()