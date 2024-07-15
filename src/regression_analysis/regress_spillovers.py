import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from stargazer.stargazer import Stargazer
from stargazer.stargazer import Label

PROJECT_DIR = Path().resolve()

# ===============================================================================
# 1. German Bunds
# ===============================================================================
ecb = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_german_spot_yields.csv')
ecb.dropna(subset=["10yr Change", "US10y Change"], inplace=True)
ecb = ecb[ecb["In Fed 3dWindow"].astype(bool)]
ecb_results = sm.OLS(ecb["10yr Change"], sm.add_constant(ecb[["US10y Change"]])).fit()
ecb_stargazer = Stargazer([ecb_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(ecb_stargazer.render_latex())

# Calculate standardized coefficient
beta = ecb_results.params["US10y Change"]
sd_x = ecb["US10y Change"].std()
sd_y = ecb["10yr Change"].std()
standardized_beta = beta * (sd_x / sd_y)

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10y Change", y="10yr Change", data=ecb, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Germany', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, DE}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = ecb_results.params["US10y Change"]
plt.text(-0.25, 0.13, rf'$\beta^*: {standardized_beta:.2f}$', fontsize=24, color='darkblue')
plt.text(-0.25, 0.17, rf'$\beta$   : {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "DE_spilloverdene.png")
plt.show()

# ===============================================================================
# 2. UK Gilts
# ===============================================================================
uk = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_uk_spot_yields.csv')
uk = uk[uk["In Fed 3dWindow"].astype(bool)]
uk.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
uk_results = sm.OLS(uk["10yr Change"], sm.add_constant(uk[["US10yr Change"]])).fit()
uk_stargazer = Stargazer([uk_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(uk_stargazer.render_latex())

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=uk, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('United Kingdom', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, UK}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = uk_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "UK_spillover.png")
plt.show()

# ===============================================================================
# 3. Japanese Bonds
# ===============================================================================
japan = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_japan_spot_yields.csv')
japan = japan[japan["In Fed 3dWindow"].astype(bool)]
japan.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
japan_results = sm.OLS(japan["10yr Change"], sm.add_constant(japan[["US10yr Change"]])).fit()
japan_stargazer = Stargazer([japan_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(japan_stargazer.render_latex())

# Calculate standardized coefficient
beta = japan_results.params["US10yr Change"]
sd_x = japan["US10yr Change"].std()
sd_y = japan["10yr Change"].std()
standardized_beta = beta * (sd_x / sd_y)

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=japan, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Japan', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, JP}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = japan_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "JP_spillover.png")
plt.show()

# ===============================================================================
# 4. Canada
# ===============================================================================
canada = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_canada_spot_yields.csv')
canada = canada[canada["In Fed 3dWindow"].astype(bool)]
canada["10yr Change"] = canada["10yr Change"] * 100
canada.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
canada_results = sm.OLS(canada["10yr Change"], sm.add_constant(canada[["US10yr Change"]])).fit()
canada_stargazer = Stargazer([canada_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(canada_stargazer.render_latex())

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=canada, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Canada', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, CD}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = canada_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "CD_spillover.png")
plt.show()

# ===============================================================================
# 5. Swiss Bonds
# ===============================================================================
swiss = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_swiss_spot_yields.csv')
swiss = swiss[swiss["In Fed 3dWindow"].astype(bool)]
swiss.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
swiss_results = sm.OLS(swiss["10yr Change"], sm.add_constant(swiss[["US10yr Change"]])).fit()
swiss_stargazer = Stargazer([swiss_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(swiss_stargazer.render_latex())

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=swiss, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Switzerland', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, CH}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = swiss_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "CH_spillover.png")
plt.show()

# ===============================================================================
# 6. Australian Bonds
# ===============================================================================
australia = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_australia_spot_yields.csv')
australia = australia[australia["In Fed 3dWindow"].astype(bool)]
#australia["10yr Change"] = australia["10yr Change"] * 100
australia.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
australia_results = sm.OLS(australia["10yr Change"], sm.add_constant(australia[["US10yr Change"]])).fit()
australia_stargazer = Stargazer([australia_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(australia_stargazer.render_latex())

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=australia, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Australia', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, AU}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = australia_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "AU_spillover.png")
plt.show()


#TODO: only after-2008
japan = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'reg_japan_spot_yields.csv')
japan.set_index("Date", inplace=True)
japan.index = pd.to_datetime(japan.index)
japan = japan.loc[japan.index >= '2008-01-01']
japan = japan[japan["In Fed 3dWindow"].astype(bool)]
japan.dropna(subset=["10yr Change", "US10yr Change"], inplace=True)
japan_results = sm.OLS(japan["10yr Change"], sm.add_constant(japan[["US10yr Change"]])).fit()
japan_stargazer = Stargazer([japan_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'bund_spillover.tex', 'w') as file:
    file.write(japan_stargazer.render_latex())

# Create the scatter plot with regression line and 95% confidence interval
plt.figure(figsize=(10, 6))
sns.regplot(x="US10yr Change", y="10yr Change", data=japan, ci=95, scatter_kws={"color" : "black", "alpha":0.6}, line_kws={"color": "red"})
plt.title('Japan', fontsize=28)
plt.xlabel(r'$\Delta 10yr_{t-1,t, US}$', fontsize=24)
plt.ylabel(r'$\Delta 10yr_{t-1,t, JP}$', fontsize=24)
plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axhline(0, color='black', linewidth=2)  # Bolder line
plt.axvline(0, color='black', linewidth=2)  # Bolder line
coef = japan_results.params["US10yr Change"]
plt.text(-0.25, 0.15, rf'$\beta$: {coef:.2f}', fontsize=24, color='darkblue')
plt.savefig(PROJECT_DIR / "figs" / "spillover_scatters" / "JP_2008_spillover.png")
plt.show()