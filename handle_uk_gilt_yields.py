import pandas as pd
from pathlib import Path

PROJECT_DIR = Path().resolve()

data7984 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_1979 to 1984.xlsx',
                        sheet_name='4. nominal spot curve',
                        index_col=0)

data8589 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_1985 to 1989.xlsx',
                        sheet_name='4. nominal spot curve', 
                        index_col=0)

data9094 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_1990 to 1994.xlsx',
                        sheet_name='4. nominal spot curve',
                        index_col=0)

data9599 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_1995 to 1999.xlsx',
                        sheet_name='4. nominal spot curve',
                        index_col=0)

data0004 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_2000 to 2004.xlsx',
                        sheet_name='4. nominal spot curve',
                        index_col=0)

data0515 = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_2005 to 2015.xlsx',
                        sheet_name='4. spot curve',
                        index_col=0)

data16p = pd.read_excel(PROJECT_DIR / 'original_data' / 'boe_gilt_yields' / 'GLC Nominal daily data_2016 to present.xlsx',
                        sheet_name='4. spot curve',
                        index_col=0)

frames = [data7984, data8589, data9094, data9599, data0004, data0515, data16p]
result = pd.concat(frames)

# there are some completely missing dates although there are indices for them
empty_row_indices = result[result.isnull().all(axis=1)].index
print('Indices of completely empty rows:', empty_row_indices)

result.columns = [f"{col}yr" if isinstance(col, float) else col for col in result.columns]
result.rename(columns={
    '1.0yr' : '1yr',
    '2.0yr' : '2yr',
    '3.0yr' : '3yr',
    '4.0yr' : '4yr',
    '5.0yr' : '5yr',
    '6.0yr' : '6yr',
    '7.0yr' : '7yr',
    '8.0yr' : '8yr',
    '9.0yr' : '9yr',
    '10.0yr' : '10yr',
    '12.0yr' : '12yr',
    '15.0yr' : '15yr',
    '20.0yr' : '20yr',
    '25.0yr' : '25yr',
    '30.0yr' : '30yr',
    '40.0yr' : '40yr',
}, inplace=True)

result.to_csv(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_spot_yields.csv', index=True)
result.to_pickle(PROJECT_DIR / 'processed_data' / 'yield_data' / 'uk_spot_yields.pkl')