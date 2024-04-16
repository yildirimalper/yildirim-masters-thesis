import pandas as pd
from pandas.tseries.offsets import Day

def create_3d_window(date):
    """
    Create a list of dates that are within a three-day window around a given date.
    """
    return pd.date_range(start=date - Day(1), end=date + Day(1))

def create_5d_window(date):
    """
    Create a 5-day window around a date.
    """
    return pd.date_range(start=date - pd.Timedelta(days=2), end=date + pd.Timedelta(days=2))

def create_7d_window(date):
    """
    Create a 7-day window around a date.
    """
    return pd.date_range(start=date - pd.Timedelta(days=3), end=date + pd.Timedelta(days=3))