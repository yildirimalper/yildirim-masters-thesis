import pandas as pd
from pathlib import Path

PROJECT_DIR = Path().resolve()

# ==================================================================0
# USD-EUR Exchange Rates
# ==================================================================0
usdeur1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdeur-2009-2024.csv")
usdeur1.rename(columns= {"Tarih":"Date", "Şimdi":"Price", "Açılış":"Open", "Yüksek":"High", "Düşük":"Low", "Hac.":"Vol.", "Fark %":"Change %"}, inplace=True)
usdeur1["Date"] = pd.to_datetime(usdeur1["Date"])

usdeur2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdeur-1993-2008.csv")
usdeur2.rename(columns= {"Tarih":"Date", "Şimdi":"Price", "Açılış":"Open", "Yüksek":"High", "Düşük":"Low", "Hac.":"Vol.", "Fark %":"Change %"}, inplace=True)
usdeur2["Date"] = pd.to_datetime(usdeur2["Date"])

usdeur = pd.concat([usdeur1, usdeur2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdeur.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdeur.csv", index=False)
usdeur.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdeur.pkl")

# ==================================================================0
# USD-GBP Exchange Rates
# ==================================================================0
usdgbp1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdgbp-2009-2024.csv")
usdgbp1["Date"] = pd.to_datetime(usdgbp1["Date"])

usdgbp2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdgbp-1993-2008.csv")
usdgbp2["Date"] = pd.to_datetime(usdgbp2["Date"])

usdgbp = pd.concat([usdgbp1, usdgbp2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdgbp.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdgbp.csv", index=False)
usdgbp.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdgbp.pkl")

# ==================================================================0
# USD-JPY Exchange Rates
# ==================================================================0
usdjpy1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdjpy-2009-2024.csv")
usdjpy1["Date"] = pd.to_datetime(usdjpy1["Date"])

usdjpy2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdjpy-1993-2008.csv")
usdjpy2["Date"] = pd.to_datetime(usdjpy2["Date"])

usdjpy = pd.concat([usdjpy1, usdjpy2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdjpy.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdjpy.csv", index=False)
usdjpy.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdjpy.pkl")

# ==================================================================0
# USD-CAD Exchange Rates
# ==================================================================0
usdcad1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdcad-2009-2024.csv")
usdcad1["Date"] = pd.to_datetime(usdcad1["Date"])

usdcad2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdcad-1993-2008.csv")
usdcad2["Date"] = pd.to_datetime(usdcad2["Date"])

usdcad = pd.concat([usdcad1, usdcad2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdcad.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdcad.csv", index=False)
usdcad.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdcad.pkl")

# ==================================================================0
# USD-CHF Exchange Rates
# ==================================================================0
usdchf1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdchf-2009-2024.csv")
usdchf1["Date"] = pd.to_datetime(usdchf1["Date"])

usdchf2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdchf-1993-2008.csv")
usdchf2["Date"] = pd.to_datetime(usdchf2["Date"])

usdchf = pd.concat([usdchf1, usdchf2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdchf.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdchf.csv", index=False)
usdchf.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdchf.pkl")

# ==================================================================0
# USD-AUD Exchange Rates
# ==================================================================0
usdaud1 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdaud-2009-2024.csv")
usdaud1["Date"] = pd.to_datetime(usdaud1["Date"])

usdaud2 = pd.read_csv(PROJECT_DIR / "original_data" / "exchange_rates" / "usdaud-1993-2008.csv")
usdaud2["Date"] = pd.to_datetime(usdaud2["Date"])

usdaud = pd.concat([usdaud1, usdaud2], ignore_index=True).sort_values(by="Date", ascending=False).reset_index(drop=True)
usdaud.to_csv(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdaud.csv", index=False)
usdaud.to_pickle(PROJECT_DIR / "processed_data" / "exchange_rates" / "usdaud.pkl")
