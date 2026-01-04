import os
import json
import pandas as pd
from datetime import datetime
from src.data_manager import DataManager

# Constants
CACHE_DIR = "data/cache"
DAILY_NAV_CACHE = os.path.join(CACHE_DIR, "nav_cache.json")
INDEX_CACHE = os.path.join(CACHE_DIR, "index_cache.json")

def sync():
    os.makedirs(CACHE_DIR, exist_ok=True)
    dm = DataManager()
    
    # In a real app, we'd get these from the DB or a list of active schemes
    # For now, let's sync common indices
    indices = {
        "Nifty 50": "^NSEI",
        "Nifty Next 50": "^NSMIDCP50"
    }
    
    index_data = {}
    print("Syncing market indices...")
    for name, ticker in indices.items():
        print(f"  Fetching {name}...")
        hist = dm.fetch_index_data(ticker, "2020-01-01")
        if not hist.empty:
            index_data[ticker] = hist.to_dict()
            
    with open(INDEX_CACHE, 'w') as f:
        json.dump(index_data, f, default=str)
        
    print("\nSync complete.")

if __name__ == "__main__":
    sync()
