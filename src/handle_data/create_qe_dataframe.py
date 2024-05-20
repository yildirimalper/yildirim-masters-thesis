import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_DIR = Path().resolve()

# Create a DataFrame with dates from 1990Q1 to 2024Q2
dates = pd.date_range(start='1990Q1', end='2024Q2', freq='D')
df = pd.DataFrame(  index=dates, 
                    columns=["QE - ECB", "QE - BoE", "QE - SNB", 
                        "QE - RBA", "QE - BoC", "QE - BoJ",
                        "QE - Fed"])
df.reset_index(inplace=True)
df.rename(columns={'index': 'Date'}, inplace=True)

df.loc[:, df.columns != 'Date'] = 0

# Fill QE dates in the US with 1
df.loc[(df['Date'] >= '2008-11-25') & (df['Date'] <= '2010-03-31'), 'QE - Fed'] = 1
df.loc[(df['Date'] >= '2010-11-03') & (df['Date'] <= '2011-06-30'), 'QE - Fed'] = 1
df.loc[(df['Date'] >= '2012-09-13') & (df['Date'] <= '2014-10-29'), 'QE - Fed'] = 1

# Fill QE dates in the UK with 1
df.loc[(df['Date'] >= '2009-03-05') & (df['Date'] <= '2010-01-31'), 'QE - BoE'] = 1
df.loc[(df['Date'] >= '2011-10-07') & (df['Date'] <= '2012-11-08'), 'QE - BoE'] = 1
df.loc[(df['Date'] >= '2012-07-05') & (df['Date'] <= '2012-09-05'), 'QE - BoE'] = 1

# Fill QE dates in Japan with 1
df.loc[(df['Date'] >= '2001-03-09') & (df['Date'] <= '2006-03-09'), 'QE - BoJ'] = 1

#TODO: Check the dates for the other countries
#TODO: How to deal with SNB's 2015 currency intervention move?
#TODO: How to integrate COVID-19 era QE into the model?

# Export final data
df.to_csv(PROJECT_DIR / 'processed_data' / 'qe_df.csv', index=False)