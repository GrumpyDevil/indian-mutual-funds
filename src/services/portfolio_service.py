import pandas as pd
import os
from datetime import datetime
from ..finance import safe_xirr, aggregate_units, get_market_value
from ..data_manager import DataManager

class PortfolioService:
    def __init__(self, transactions_file: str, manual_mapping: dict = None):
        self.transactions_file = transactions_file
        self.dm = DataManager(manual_mapping=manual_mapping)

    def sanitize(self, val):
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

    def get_portfolio_summary(self):
        if not os.path.exists(self.transactions_file):
            return {"error": "Transactions file not found"}

        df = pd.read_excel(self.transactions_file, sheet_name='Sheet1')
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Sign management
        import numpy as np
        df['Effective Units'] = df['Units'].abs() * np.sign(df['Actual Amount'])
        
        unique_schemes = df['Scheme Name'].unique()
        
        today = datetime.now()
        portfolio_cfs = [] 
        for _, row in df.iterrows():
            portfolio_cfs.append((row['Date'], -row['Actual Amount']))
            
        current_portfolio_value = 0
        fund_details = []
        
        for s in unique_schemes:
            units = aggregate_units(df, s)
            invested_in_fund = df[df['Scheme Name'] == s]['Actual Amount'].sum()
            
            code = self.dm.find_best_match(s)
            curr_nav = self.dm.fetch_current_nav(code) if code else 0
            curr_val = get_market_value(units, curr_nav)
            
            current_portfolio_value += curr_val
            if abs(units) > 0.001 or abs(invested_in_fund) > 1:
                fund_details.append({
                    "scheme": s,
                    "units": units,
                    "net_capital": invested_in_fund,
                    "value": curr_val,
                    "returns_pct": (curr_val / invested_in_fund - 1) * 100 if invested_in_fund > 0 else 0
                })
        
        portfolio_cfs.append((today, current_portfolio_value))
        xirr_val = safe_xirr(portfolio_cfs)
        
        net_capital = df['Actual Amount'].sum()

        holdings_sanitized = []
        for h in fund_details:
            holdings_sanitized.append({
                "scheme": str(h["scheme"]),
                "units": self.sanitize(h["units"]),
                "net_capital": self.sanitize(h["net_capital"]),
                "value": self.sanitize(h["value"]),
                "returns_pct": self.sanitize(h["returns_pct"])
            })

        result = {
            "summary": {
                "current_value": self.sanitize(current_portfolio_value),
                "net_capital_invested": self.sanitize(net_capital),
                "total_profit_loss": self.sanitize(current_portfolio_value - net_capital),
                "xirr": self.sanitize(xirr_val)
            },
            "holdings": holdings_sanitized
        }
        return result

    def get_sip_performance(self):
        """Get SIP performance trajectory with benchmark comparisons"""
        if not os.path.exists(self.transactions_file):
            return {"error": "Transactions file not found"}

        df = pd.read_excel(self.transactions_file, sheet_name='Sheet1')
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        import numpy as np
        
        # Get the earliest transaction date for benchmark data
        start_date = df['Date'].min()
        
        # Get benchmark data
        nifty50_price = self.dm.fetch_index_data("^NSEI", start_date=start_date, normalize=True)
        nifty50_tri = self.dm.fetch_index_data("^NSETR", start_date=start_date, normalize=True)
        
        trajectory = []
        cumulative_invested = 0
        current_holdings = {}  # scheme_name -> units
        
        # Benchmark SIP tracking
        nifty_price_units = 0
        nifty_tri_units = 0
        
        unique_dates = sorted(df['Date'].unique())
        
        # Pre-fetch historical NAVs for all schemes
        scheme_navs = {}
        unique_schemes = df['Scheme Name'].unique()
        for s in unique_schemes:
            code = self.dm.find_best_match(s)
            if code:
                scheme_navs[s] = self.dm.fetch_historical_nav(code)

        for date in unique_dates:
            day_txs = df[df['Date'] == date]
            day_investment = 0
            
            for _, row in day_txs.iterrows():
                amount = row['Actual Amount']
                cumulative_invested += amount
                day_investment += amount
                s = row['Scheme Name']
                current_holdings[s] = current_holdings.get(s, 0) + row['Units']
            
            # Calculate portfolio market value
            market_value = 0
            for s, units in current_holdings.items():
                if abs(units) < 0.001: continue
                navs = scheme_navs.get(s)
                if navs is not None and not navs.empty:
                    try:
                        hist_nav = navs.asof(date)
                        if hist_nav is not None and not np.isnan(hist_nav):
                            market_value += float(units) * float(hist_nav)
                    except:
                        pass
            
            # Calculate benchmark values
            nifty_price_value = 0
            nifty_tri_value = 0
            
            if day_investment > 0:
                # Buy benchmark units with same investment
                try:
                    price_nav = nifty50_price.asof(date) if not nifty50_price.empty else None
                    if price_nav is not None and not np.isnan(price_nav) and price_nav > 0:
                        nifty_price_units += day_investment / float(price_nav)
                except:
                    pass
                
                try:
                    tri_nav = nifty50_tri.asof(date) if not nifty50_tri.empty else None
                    if tri_nav is not None and not np.isnan(tri_nav) and tri_nav > 0:
                        nifty_tri_units += day_investment / float(tri_nav)
                except:
                    pass
            
            # Current benchmark values
            try:
                price_nav = nifty50_price.asof(date) if not nifty50_price.empty else None
                if price_nav is not None and not np.isnan(price_nav):
                    nifty_price_value = nifty_price_units * float(price_nav)
            except:
                pass
            
            try:
                tri_nav = nifty50_tri.asof(date) if not nifty50_tri.empty else None
                if tri_nav is not None and not np.isnan(tri_nav):
                    nifty_tri_value = nifty_tri_units * float(tri_nav)
            except:
                pass
            
            trajectory.append({
                "date": date.strftime('%Y-%m-%d'),
                "invested": self.sanitize(cumulative_invested),
                "portfolio_value": self.sanitize(market_value),
                "nifty50_price": self.sanitize(nifty_price_value),
                "nifty50_tri": self.sanitize(nifty_tri_value)
            })
            
        return trajectory
