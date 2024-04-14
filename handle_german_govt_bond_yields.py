import pandas as pd
from pathlib import Path

PROJECT_DIR = Path().resolve()

data1y = pd.read_csv(PROJECT_DIR / "original_data" / "germany1y.csv")
data1y["Date"] = pd.to_datetime(data1y["Date"])
data1y = data1y.drop(columns=["Open", "High", "Low", "Change %"])
data1y = data1y.rename(columns={"Price": "1y Yield"})

data2y = pd.read_csv(PROJECT_DIR / "original_data" / "germany2y.csv")
data2y["Date"] = pd.to_datetime(data2y["Date"])
data2y = data2y.drop(columns=["Open", "High", "Low", "Change %"])
data2y = data2y.rename(columns={"Price": "2y Yield"})

data5y = pd.read_csv(PROJECT_DIR / "original_data" / "germany5y.csv")
data5y["Date"] = pd.to_datetime(data5y["Date"])
data5y = data5y.drop(columns=["Open", "High", "Low", "Change %"])
data5y = data5y.rename(columns={"Price": "5y Yield"})

data10y = pd.read_csv(PROJECT_DIR / "original_data" / "germany10y.csv")
data10y["Date"] = pd.to_datetime(data10y["Date"])
data10y = data10y.drop(columns=["Open", "High", "Low", "Change %"])
data10y = data10y.rename(columns={"Price": "10y Yield"})

data20y = pd.read_csv(PROJECT_DIR / "original_data" / "germany20y.csv")
data20y["Date"] = pd.to_datetime(data20y["Date"])
data20y = data20y.drop(columns=["Open", "High", "Low", "Change %"])
data20y = data20y.rename(columns={"Price": "20y Yield"})

data30y = pd.read_csv(PROJECT_DIR / "original_data" / "germany30y.csv")
data30y["Date"] = pd.to_datetime(data30y["Date"])
data30y = data30y.drop(columns=["Open", "High", "Low", "Change %"])
data30y = data30y.rename(columns={"Price": "30y Yield"})

data_1_2 = data1y.merge(data2y, on="Date", how="inner")
data_1_2_5 = data_1_2.merge(data5y, on="Date", how="inner")
data_1_2_5_10 = data_1_2_5.merge(data10y, on="Date", how="inner")
data_1_2_5_10_20 = data_1_2_5_10.merge(data20y, on="Date", how="inner")
data = data_1_2_5_10_20.merge(data30y, on="Date", how="inner")

data = data.sort_values(by="Date")

data.to_csv(PROJECT_DIR / "processed_data" / "german_govt_bond_yields.csv", index=False)
data.to_pickle(PROJECT_DIR / "processed_data" / "german_govt_bond_yields.pkl")