import pandas as pd
import numpy as np
from datetime import datetime
from .finance import safe_xirr

def simulate_benchmark_sip(transactions_df, benchmark_nav_history, today=None):
    """
    Simulate buying benchmark units on the same dates as portfolio transactions.
    
    Returns:
        tuple: (units, current_value, xirr, cashflows)
    """
    if today is None:
        today = datetime.now()
        
    benchmark_units = 0
    benchmark_cfs = []
    
    for _, row in transactions_df.iterrows():
        date = row['Date']
        amount = row['Actual Amount']
        
        benchmark_cfs.append((date, -amount))
        
        nav = get_nav_on_date(benchmark_nav_history, date)
        if not np.isnan(nav):
            benchmark_units += amount / nav
            
    current_nav = benchmark_nav_history.iloc[-1]
    current_val = benchmark_units * current_nav
    
    benchmark_cfs.append((today, current_val))
    benchmark_xirr = safe_xirr(benchmark_cfs)
    
    return benchmark_units, current_val, benchmark_xirr, benchmark_cfs

def get_nav_on_date(nav_history, target_date):
    """
    Get NAV on or before the target date.
    nav_history should be a Series with DatetimeIndex, sorted ascending.
    """
    if target_date in nav_history.index:
        val = nav_history.loc[target_date]
        if isinstance(val, pd.Series): # Handle duplicates
            return val.iloc[0]
        return val
    
    # Find the nearest date before the target_date
    past_dates = nav_history.index[nav_history.index <= target_date]
    if not past_dates.empty:
        val = nav_history.loc[past_dates[-1]]
        if isinstance(val, pd.Series):
            return val.iloc[0]
        return val
    
    # If no past date, find the nearest future date
    future_dates = nav_history.index[nav_history.index > target_date]
    if not future_dates.empty:
        val = nav_history.loc[future_dates[0]]
        if isinstance(val, pd.Series):
            return val.iloc[0]
        return val
    
    return np.nan
