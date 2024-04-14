import pandas as pd
import requests
from pathlib import Path

PROJECT_DIR = Path().resolve()

spot_parameters = [f"YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_{i}Y" for i in range(30, 0, -1)]
spot_parameters.append("YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_6M")

forward_parameters = [f"YC/B.U2.EUR.4F.G_N_A.SV_C_YM.IF_{i}Y" for i in range(30, 0, -1)]
forward_parameters.append("YC/B.U2.EUR.4F.G_N_A.SV_C_YM.IF_6M")

url = 'https://sdw-wsrest.ecb.europa.eu/service/data/'
headers = {'Accept':'application/json'}
#r = requests.get('{}{}'.format(url, series_key), headers=headers).json()
#print(r['structure']['dimensions']['series'])

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

# =============================================================================
# Spot bond yields
# =============================================================================

spot_dataframes = {}
for param in spot_parameters:
    spot_df = get_data(param)
    if not spot_df.empty:
        spot_dataframes[param] = spot_df

spot_df = pd.concat(spot_dataframes.values(), axis=1)
spot_df.columns = spot_dataframes.keys()

spot_column_rename_dict = {f"YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_{i}Y": f"YC - Spot - {i}y" for i in range(30, 1, -1)}
spot_column_rename_dict["YC/B.U2.EUR.4F.G_N_A.SV_C_YM.SR_6M"] = "YC - Spot - 6m"
spot_df.rename(columns=spot_column_rename_dict, inplace=True)

spot_df.to_pickle(PROJECT_DIR / 'processed_data' / 'spot_yields.pkl')
spot_df.to_csv(PROJECT_DIR / 'processed_data' / 'spot_yields.csv')

# =============================================================================
# Forward bond yields
# =============================================================================

forward_dataframes = {}
for param in forward_parameters:
    forward_df = get_data(param)
    if not forward_df.empty:
        forward_dataframes[param] = forward_df

forward_df = pd.concat(forward_dataframes.values(), axis=1)
forward_df.columns = forward_dataframes.keys()

forward_column_rename_dict = {f"YC/B.U2.EUR.4F.G_N_A.SV_C_YM.IF_{i}Y": f"YC - Forward - {i}y" for i in range(30, 1, -1)}
forward_column_rename_dict["YC/B.U2.EUR.4F.G_N_A.SV_C_YM.IF_6M"] = "YC - Forward - 6m"
forward_df.rename(columns=forward_column_rename_dict, inplace=True)

# Save the dataframe to a pickle file
forward_df.to_pickle(PROJECT_DIR / 'processed_data' / 'forward_yields.pkl')
forward_df.to_csv(PROJECT_DIR / 'processed_data' / 'forward_yields.csv')