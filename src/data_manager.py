import pandas as pd
import yfinance as yf
from mftool import Mftool
from thefuzz import process, fuzz
from datetime import datetime

class DataManager:
    def __init__(self, manual_mapping=None):
        self.mf = Mftool()
        self.manual_mapping = manual_mapping or {}
        self._all_schemes = None

    def get_all_schemes(self):
        if self._all_schemes is None:
            self._all_schemes = self.mf.get_scheme_codes()
        return self._all_schemes

    def find_best_match(self, name):
        if name in self.manual_mapping:
            return self.manual_mapping[name]
        
        choices = self.get_all_schemes()
        names = list(choices.values())
        
        # Try exact match first
        for code, n in choices.items():
            if n.lower() == name.lower():
                return code
                
        # Try fuzzy match
        match, score = process.extractOne(name, names, scorer=fuzz.WRatio)
        if score > 80:
            for code, n in choices.items():
                if n == match:
                    return code
        return None

    def fetch_current_nav(self, scheme_code):
        try:
            q = self.mf.get_scheme_quote(scheme_code)
            if 'last_updated_nav' in q:
                return float(q['last_updated_nav'])
        except Exception:
            pass
            
        try:
            hist = self.mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
            if hist is not None and not hist.empty:
                return float(hist['nav'].iloc[0])
        except Exception:
            pass
        return 0.0

    def fetch_historical_nav(self, scheme_code, normalize=True):
        """
        Fetch historical NAV and optionally normalize (forward-fill missing dates).
        """
        hist = pd.Series()
        try:
            hist = self.mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
            if hist is not None and not hist.empty:
                hist.index = pd.to_datetime(hist.index, dayfirst=True)
                hist = hist.sort_index()
                hist = hist['nav'].astype(float)
        except Exception:
            pass

        if normalize and not hist.empty:
            # Reindex to daily frequency and forward-fill
            all_dates = pd.date_range(start=hist.index.min(), end=datetime.now())
            hist = hist.reindex(all_dates).ffill()
            
        return hist

    def fetch_index_data(self, ticker, start_date, normalize=True):
        """
        Fetch index data and optionally normalize.
        """
        hist = pd.Series()
        try:
            data = yf.download(ticker, start=start_date)
            if not data.empty:
                hist = data['Close'].squeeze()
                if isinstance(hist, pd.DataFrame): # Handle potential multi-index or multiple columns
                    hist = hist.iloc[:, 0]
        except Exception:
            pass

        if normalize and not hist.empty:
            all_dates = pd.date_range(start=hist.index.min(), end=datetime.now())
            hist = hist.reindex(all_dates).ffill()

        return hist
