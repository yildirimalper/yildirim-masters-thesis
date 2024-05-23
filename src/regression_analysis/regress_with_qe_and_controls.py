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
ecb["In ECB 3dWindow"] = ecb["In ECB 3dWindow"].astype(int)
ecb["In Fed 3dWindow"] = ecb["In Fed 3dWindow"].astype(int)
ecb_results = sm.OLS(ecb["10yr Change"], 
                    sm.add_constant(ecb[["In ECB 3dWindow", "In Fed 3dWindow", "ECB - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
ecb_stargazer = Stargazer([ecb_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'ecb_regression_c.tex', 'w') as file:
    file.write(ecb_stargazer.render_latex())

# ===============================================================================
# 2. Bank of England
# ===============================================================================
boe = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_uk_spot_yields.csv')
boe = boe.dropna()
boe["In BoE 3dWindow"] = boe["In BoE 3dWindow"].astype(int)
boe["In Fed 3dWindow"] = boe["In Fed 3dWindow"].astype(int)
boe_results = sm.OLS(boe["10yr Change"], 
                    sm.add_constant(boe[["In BoE 3dWindow", "In Fed 3dWindow", "BoE - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
boe_stargazer = Stargazer([boe_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boe_regression_c.tex', 'w') as file:
    file.write(boe_stargazer.render_latex())

# ===============================================================================
# 3. Bank of Japan
# ===============================================================================
boj = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_japanese_spot_yields.csv')
boj = boj.dropna()
boj["In BoJ 3dWindow"] = boj["In BoJ 3dWindow"].astype(int)
boj["In Fed 3dWindow"] = boj["In Fed 3dWindow"].astype(int)
boj_results = sm.OLS(boj["10yr Change"],
                    sm.add_constant(boj[["In BoJ 3dWindow", "In Fed 3dWindow", "BoJ - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
boj_stargazer = Stargazer([boj_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boj_regression_c.tex', 'w') as file:
    file.write(boj_stargazer.render_latex())

# ===============================================================================
# 4. Swiss National Bank
# ===============================================================================
snb = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_swiss_spot_yields.csv')
snb = snb.dropna() # only 1 obs in 10yr Change is NA
snb["In SNB 3dWindow"] = snb["In SNB 3dWindow"].astype(int)
snb["In Fed 3dWindow"] = snb["In Fed 3dWindow"].astype(int)
snb_results = sm.OLS(snb["10yr Change"],
                        sm.add_constant(snb[["In SNB 3dWindow", "In Fed 3dWindow", "SNB - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
snb_stargazer = Stargazer([snb_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'snb_regression_c.tex', 'w') as file:
    file.write(snb_stargazer.render_latex())

# ===============================================================================
# 5. Reserve Bank of Australia
# ===============================================================================
rba = pd.read_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'proc_australian_spot_yields.csv')
rba = rba.dropna()
rba["In RBA 3dWindow"] = rba["In RBA 3dWindow"].astype(int)
rba["In Fed 3dWindow"] = rba["In Fed 3dWindow"].astype(int)
rba_results = sm.OLS(rba["10yr Change"],
                    sm.add_constant(rba[["In RBA 3dWindow", "In Fed 3dWindow", "RBA - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
rba_stargazer = Stargazer([rba_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'rba_regression_c.tex', 'w') as file:
    file.write(rba_stargazer.render_latex())

# ===============================================================================
# 6. Bank of Canada
# ===============================================================================
boc = pd.read_csv(PROJECT_DIR / 'processed_data' / 'proc_canadian_spot_yields.csv')
boc = boc.dropna()
boc["In BoC 3dWindow"] = boc["In BoC 3dWindow"].astype(int)
boc["In Fed 3dWindow"] = boc["In Fed 3dWindow"].astype(int)
boe_results = sm.OLS(boc["10yr Change"],
                    sm.add_constant(boc[["In BoC 3dWindow", "In Fed 3dWindow", "BoC - QE", "Fed - QE", "dxy", "igrea", "vix"]])).fit()
boe_stargazer = Stargazer([boe_results])
with open(PROJECT_DIR / 'paper' / 'tables' / 'boc_regression_c.tex', 'w') as file:
    file.write(boe_stargazer.render_latex())

# ===============================================================================
# Aggregate LaTeX Output
# ===============================================================================
stargazer = Stargazer([ecb_results, boe_results, boj_results, snb_results, rba_results])
stargazer.title("Regression Results")
# without BoC here
stargazer.custom_columns(['ECB', 'BoE', 'BoJ', 'SNB', 'RBA', 'BoC'], [1, 1, 1, 1, 1, 1])
stargazer.show_model_numbers(False)
stargazer.show_degrees_of_freedom(False)
stargazer.rename_covariates({'10yr Change': Label({'LaTeX' : '$\Delta$ 10yr'}), 'const': 'Intercept'})
with open(PROJECT_DIR / 'paper' / 'tables' / 'regression_results_c.tex', 'w') as file:
    file.write(stargazer.render_latex())