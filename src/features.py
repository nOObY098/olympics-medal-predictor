# features.py
# Feature engineering functions for the Olympics medal predictor.
# Fill this in during Phase 2.

import pandas as pd
import numpy as np


# --- Host nation flag ---

def add_host_flag(df, country_col, year_col, host_map):
    """
    Add a binary is_host column based on a year-to-country mapping.

    Parameters
    ----------
    df         : pd.DataFrame
    country_col: str — column with NOC country codes
    year_col   : str — column with Olympic year
    host_map   : dict — {year: NOC} e.g. {2020: 'JPN'}

    Returns
    -------
    pd.DataFrame with new is_host column
    """
    df = df.copy()
    df['is_host'] = df.apply(
        lambda row: 1 if host_map.get(row[year_col]) == row[country_col] else 0,
        axis=1
    )
    return df


# --- Rolling medal average ---

def add_rolling_average(df, country_col, year_col, medal_col, window=3):
    """
    Add a rolling average of past medal counts per country.
    Uses shift(1) to avoid data leakage — only uses past games.

    Parameters
    ----------
    df         : pd.DataFrame
    country_col: str
    year_col   : str
    medal_col  : str — column to average (e.g. 'total')
    window     : int — number of past games to average over

    Returns
    -------
    pd.DataFrame with new rolling_avg column
    """
    df = df.copy().sort_values([country_col, year_col])
    df['rolling_avg'] = (
        df.groupby(country_col)[medal_col]
        .transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    )
    return df
