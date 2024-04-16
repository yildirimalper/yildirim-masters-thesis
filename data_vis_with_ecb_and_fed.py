import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path().resolve()
data = pd.read_pickle(PROJECT_DIR / 'processed_data' / 'spot_yields.pkl')
data.index = pd.to_datetime(data.index)

column_names = ["ECB Dates"]
mpdd = pd.read_csv("processed_data/monetary_policy_decision_dates.csv", header=None, names=column_names)
mpdd["MP Dates"] = pd.to_datetime(mpdd["MP Dates"])
