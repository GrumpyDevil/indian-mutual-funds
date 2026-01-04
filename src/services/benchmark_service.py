import pandas as pd
from datetime import datetime
from ..benchmark import simulate_benchmark_sip
from ..data_manager import DataManager

class BenchmarkService:
    def __init__(self, dm: DataManager):
        self.dm = dm

    def get_benchmark_comparison(self, transactions_df: pd.DataFrame, ticker: str, tri_code: str = None):
        today = datetime.now()
        start_date = transactions_df['Date'].min().strftime('%Y-%m-%d')
        
        # Index Price only
        index_nav = self.dm.fetch_index_data(ticker, start_date)
        _, val_price, xirr_price, _ = simulate_benchmark_sip(transactions_df, index_nav, today)
        
        # Index TRI
        xirr_tri = None
        val_tri = None
        if tri_code:
            tri_nav = self.dm.fetch_historical_nav(tri_code)
            _, val_tri, xirr_tri, _ = simulate_benchmark_sip(transactions_df, tri_nav, today)
            
        def sanitize(val):
            import numpy as np
            if val is None:
                return None
            if isinstance(val, (np.float64, np.float32, np.int64, np.int32)):
                val = float(val)
            if isinstance(val, (float, np.floating)):
                if np.isnan(val) or np.isinf(val):
                    return None
                return float(val)
            if isinstance(val, (int, np.integer)):
                return int(val)
            return str(val) if not isinstance(val, (dict, list, str, bool)) else val

        return {
            "index": ticker,
            "comparison": {
                "price": {"value": sanitize(val_price), "xirr": sanitize(xirr_price)},
                "tri": {"value": sanitize(val_tri), "xirr": sanitize(xirr_tri)} if tri_code else None
            }
        }
