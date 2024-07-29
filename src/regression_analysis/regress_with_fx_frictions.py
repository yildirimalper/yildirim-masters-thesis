import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import IV2SLS
from stargazer.stargazer import Stargazer
from stargazer.stargazer import Label

PROJECT_DIR = Path().resolve()

# ===============================================================================
# 1. Germany
# ===============================================================================
germany = pd.read_csv(PROJECT_DIR / 'processed_data' / 'master_data' / 'german_master.csv')
germany["In ECB 3dWindow"] = germany["In ECB 3dWindow"].astype(int)
germany["In Fed 3dWindow"] = germany["In Fed 3dWindow"].astype(int)
germany["Spread"] = germany["Spread"] * 100
germany["Interaction"] = germany["In Fed 3dWindow"] * germany["Spread"]
germany = germany.replace([np.inf, -np.inf], np.nan).dropna(subset=["10yr Change", "In Fed 3dWindow", "Spread", "Interaction"])
germany_results = sm.OLS(germany["10yr Change"], 
                    sm.add_constant(
                        germany[["In Fed 3dWindow",
                                "Spread", 
                                "Interaction"]])).fit()
germany_stargazer = Stargazer([germany_results])
with open(PROJECT_DIR / 'manuscript' / 'tables' / 'germany_regression_with_interaction.tex', 'w') as file:
    file.write(germany_stargazer.render_latex())

# Define the dependent variable, independent variables, and instrument
#dependent_var = germany["10yr Change"]
#independent_vars = germany[["In Fed 3dWindow", "Spread", "Interaction"]]
#instrument = germany["Market_Liquidity"]
#independent_vars = sm.add_constant(independent_vars)
#germany_2sls = IV2SLS(dependent_var, independent_vars, instrument).fit()
