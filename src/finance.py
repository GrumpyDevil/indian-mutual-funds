import numpy as np
import pandas as pd
from pyxirr import xirr

def safe_xirr(cfs):
    """
    Calculate XIRR from a list of (date, amount) tuples.
    Returns None if calculation fails or no valid cash flows exist.
    """
    try:
        if not cfs:
            return None
        dates, amounts = zip(*cfs)
        # Filter out negligible amounts
        valid_cfs = [(d, a) for d, a in zip(dates, amounts) if abs(a) > 0.01]
        if not valid_cfs:
            return None
        d, a = zip(*valid_cfs)
        return xirr(d, a)
    except Exception:
        return None

def calculate_cagr(start_value, end_value, years):
    """Calculate Compound Annual Growth Rate."""
    if start_value <= 0 or end_value <= 0 or years <= 0:
        return 0
    return (end_value / start_value) ** (1 / years) - 1

def aggregate_units(transactions_df, scheme_name):
    """
    Calculate total units for a scheme from a transactions DataFrame.
    Expected columns: 'Scheme Name', 'Effective Units'
    """
    scheme_txns = transactions_df[transactions_df['Scheme Name'] == scheme_name]
    return scheme_txns['Effective Units'].sum()

def get_market_value(units, nav):
    """Calculate market value from units and NAV."""
    return units * nav
