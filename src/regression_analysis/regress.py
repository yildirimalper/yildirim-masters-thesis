import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
from stargazer.stargazer import Stargazer
from stargazer.stargazer import Label

PROJECT_DIR = Path().resolve()

# ===============================================================================
# 1. European Central Bank
# ===============================================================================
ecb = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_ecb_spot_yields.csv')
ecb = ecb.dropna()
ecb_results = sm.OLS(ecb["In 3dWindow"], sm.add_constant(ecb["10yr Change"])).fit()
ecb_stargazer = Stargazer([ecb_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'ecb_regression.tex', 'w') as file:
    file.write(ecb_stargazer.render_latex())

# ===============================================================================
# 2. Bank of England
# ===============================================================================
boe = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_uk_spot_yields.csv')
boe = boe.dropna()
boe_results = sm.OLS(boe["In 3dWindow"], sm.add_constant(boe["10yr Change"])).fit()
boe_stargazer = Stargazer([boe_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boe_regression.tex', 'w') as file:
    file.write(boe_stargazer.render_latex())

# ===============================================================================
# 3. Bank of Japan
# ===============================================================================
boj = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_japanese_spot_yields.csv')
boj = boj.dropna() # only 1 obs in 10yr Change is NA
boj_results = sm.OLS(boj["In 3dWindow"], sm.add_constant(boj["10yr Change"])).fit()
boj_stargazer = Stargazer([boj_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boj_regression.tex', 'w') as file:
    file.write(boj_stargazer.render_latex())

# ===============================================================================
# 4. Swiss National Bank
# ===============================================================================
snb = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_swiss_spot_yields.csv')
snb = snb.dropna() # only 1 obs in 10yr Change is NA
snb_results = sm.OLS(snb["In 3dWindow"], sm.add_constant(snb["10yr Change"])).fit()
snb_stargazer = Stargazer([snb_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'snb_regression.tex', 'w') as file:
    file.write(snb_stargazer.render_latex())

# ===============================================================================
# 5. Reserve Bank of Australia
# ===============================================================================
rba = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_australian_spot_yields.csv')
rba = rba.dropna()
rba_results = sm.OLS(rba["In 3dWindow"], sm.add_constant(rba["10yr Change"])).fit()
rba_stargazer = Stargazer([rba_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'rba_regression.tex', 'w') as file:
    file.write(rba_stargazer.render_latex())

# ===============================================================================
# 6. Bank of Canada
# ===============================================================================
boc = pd.read_csv(PROJECT_DIR / 'processed_data' / 'proc_canadian_spot_yields.csv')
boc = boc.dropna()
boe_results = sm.OLS(boc["In 3dWindow"], sm.add_constant(boc["10yr Change"])).fit()
boe_stargazer = Stargazer([boe_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boc_regression.tex', 'w') as file:
    file.write(boe_stargazer.render_latex())

# ===============================================================================
# Aggregate LaTeX Output
# ===============================================================================
stargazer = Stargazer([ecb_results, boe_results, boj_results, snb_results, rba_results, boe_results])
stargazer.title("Regression Results")
stargazer.custom_columns(['ECB', 'BoE', 'BoJ', 'SNB', 'RBA', 'BoC'], [1, 1, 1, 1, 1, 1])
stargazer.show_model_numbers(False)
stargazer.show_degrees_of_freedom(False)
stargazer.rename_covariates({'10yr Change': Label({'LaTeX' : '$\Delta$ 10yr'}), 'const': 'Intercept'})
with open(PROJECT_DIR / 'paper' / 'tables' / 'regression_results.tex', 'w') as file:
    file.write(stargazer.render_latex())