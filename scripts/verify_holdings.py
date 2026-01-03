import sys
import os
import pandas as pd
from sqlalchemy import text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection

def verify():
    engine = get_db_connection()
    with engine.connect() as conn:
        print("--- Holdings Summary ---")
        query = text("""
            SELECT s.scheme_name, count(ph.id) as holdings_count 
            FROM portfolio_holdings ph 
            JOIN schemes s ON ph.scheme_code = s.scheme_code 
            GROUP BY s.scheme_name 
            ORDER BY holdings_count DESC 
            LIMIT 10
        """)
        df = pd.read_sql(query, conn)
        print(df.to_string())
        
        print("\n--- Top Holdings for a sample Quant scheme ---")
        sample_query = text("""
            SELECT company_name, sector, percentage_holding 
            FROM portfolio_holdings 
            WHERE scheme_code = (SELECT scheme_code FROM schemes WHERE scheme_name ILIKE '%quant Equity Savings Fund%' LIMIT 1)
            ORDER BY percentage_holding DESC
            LIMIT 10
        """)
        df_sample = pd.read_sql(sample_query, conn)
        print(df_sample.to_string())

if __name__ == "__main__":
    verify()
