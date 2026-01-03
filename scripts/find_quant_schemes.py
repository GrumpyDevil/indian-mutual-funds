from src.fetch_data import get_db_connection
from sqlalchemy import text
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

engine = get_db_connection()

def find_quant_schemes():
    query = text("SELECT scheme_code, scheme_name FROM schemes WHERE scheme_name ILIKE '%quant%'")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        print(f"Total Quant schemes found: {len(df)}")
        print(df.head(50).to_string())

if __name__ == "__main__":
    find_quant_schemes()
