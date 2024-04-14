import pandas as pd
import requests
from pathlib import Path

PROJECT_DIR = Path().resolve()

parameters = [
    "FM/B.U2.EUR.4F.KR.MLFR.CHG",    # marginal lending facility, change in p.p compared to previous rate, businessweek
    "FM/D.U2.EUR.4F.KR.MLFR.CHG",    # marginal lending facility, change in p.p compared to previous rate, daily
    "FM/B.U2.EUR.4F.KR.MLFR.LEV",    # marginal lending facility, level, daily - businessweek
    "FM/D.U2.EUR.4F.KR.MLFR.LEV",    # marginal lending facility, level, daily
    "FM/B.U2.EUR.4F.KR.MRR_MBR.LEV", # ECB main refinancing operations, variable rate tenders (minimum bid rate), level
    "FM/D.U2.EUR.4F.KR.MRR_MBR.LEV", # ECB main refinancing operations, variable rate tenders (minimum bid rate), level, daily
    "FM/B.U2.EUR.4F.KR.MRR_FR.LEV",  # ECB main refinancing operations, fixed rate tenders (fixed rate), level
    "FM/D.U2.EUR.4F.KR.MRR_FR.LEV",  # ECB main refinancing operations, fixed rate tenders (fixed rate), level, daily
    "FM/D.U2.EUR.4F.KR.MRR_RT.LEV",  # ECB main refinancing operations, level, daily
    "FM/B.U2.EUR.4F.KR.MRR.CHG",     # ECB main refinancing operations, change in p.p compared to previous rate
    "FM/B.U2.EUR.4F.KR.DFR.CHG",     # deposit facility rate, change in p.p compared to previous rate
    "FM/D.U2.EUR.4F.KR.DFR.CHG",     # deposit facility rate, change in p.p compared to previous rate, daily
    "FM/B.U2.EUR.4F.KR.DFR.LEV",     # deposit facility rate, level
    "FM/D.U2.EUR.4F.KR.DFR.LEV",     # deposit facility rate, level, daily
]

url = 'https://sdw-wsrest.ecb.europa.eu/service/data/'
headers = {'Accept':'application/json'}

def get_data(series_key):
    try:
        r = requests.get(f'{url}{series_key}', headers=headers)
        if r.status_code == 200:
            r = r.json()
            date_list = r['structure']['dimensions']['observation'][0]['values']
            dates = {i: v['id'] for i, v in enumerate(date_list)}    
            areas = [v['name'] for v in r['structure']['dimensions']['series'][4]['values']]
            df = pd.DataFrame()
            s_key = '0:0:0:0:0:0:0'
            if s_key in r['dataSets'][0]['series']:
                s_list = r['dataSets'][0]['series'][s_key]['observations']
                for i, area in enumerate(areas):
                    df[area] = pd.Series({dates[int(i)]: v[0] for i, v in s_list.items()})
                print(f"Data fetched successfully for series key {series_key}")
                return df
            else:
                print(f"Key {s_key} not found in series for series key {series_key}")
                return pd.DataFrame()
        else:
            print(f"Request for {series_key} failed with status code {r.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching data for series key {series_key}: {e}")
        return pd.DataFrame()


dataframes = {}
for param in parameters:
    df = get_data(param)
    if not df.empty:
        dataframes[param] = df

df = pd.concat(dataframes.values(), axis=1)
df.columns = dataframes.keys()

df.rename(columns={
    "FM/B.U2.EUR.4F.KR.MLFR.CHG": "Marginal Lending Facility - Change - Businessweek",
    "FM/D.U2.EUR.4F.KR.MLFR.CHG": "Marginal Lending Facility - Change - Daily",
    "FM/B.U2.EUR.4F.KR.MLFR.LEV": "Marginal Lending Facility - Level - Businessweek",
    "FM/D.U2.EUR.4F.KR.MLFR.LEV": "Marginal Lending Facility - Level - Daily",
    "FM/B.U2.EUR.4F.KR.MRR_MBR.LEV": "Main Refinancing Operations - Variable Rate Tenders - Level",
    "FM/D.U2.EUR.4F.KR.MRR_MBR.LEV": "Main Refinancing Operations - Variable Rate Tenders - Level - Daily",
    "FM/B.U2.EUR.4F.KR.MRR_FR.LEV": "Main Refinancing Operations - Fixed Rate Tenders - Level",
    "FM/D.U2.EUR.4F.KR.MRR_FR.LEV": "Main Refinancing Operations - Fixed Rate Tenders - Level - Daily",
    "FM/D.U2.EUR.4F.KR.MRR_RT.LEV": "Main Refinancing Operations - Level - Daily",
    "FM/B.U2.EUR.4F.KR.MRR.CHG": "Main Refinancing Operations - Change",
    "FM/B.U2.EUR.4F.KR.DFR.CHG": "Deposit Facility Rate - Change",
    "FM/D.U2.EUR.4F.KR.DFR.CHG": "Deposit Facility Rate - Change - Daily",
    "FM/B.U2.EUR.4F.KR.DFR.LEV": "Deposit Facility Rate - Level",
    "FM/D.U2.EUR.4F.KR.DFR.LEV": "Deposit Facility Rate - Level - Daily"
}, inplace=True)

df.to_pickle(PROJECT_DIR / 'processed_data' / 'key_interest_rates.pkl')
df.to_csv(PROJECT_DIR / 'processed_data' / 'key_interest_rates.csv')