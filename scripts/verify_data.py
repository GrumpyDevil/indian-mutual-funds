import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection
from sqlalchemy import text
import pandas as pd

engine = get_db_connection()

with engine.connect() as conn:
    print("--- Schemes Count ---")
    result = conn.execute(text("SELECT count(*) FROM schemes"))
    print(result.scalar())
    
    print("\n--- Sample Schemes ---")
    df = pd.read_sql(text("SELECT * FROM schemes LIMIT 5"), conn)
    print(df)
    
    print("\n--- NAV History Count ---")
    result = conn.execute(text("SELECT count(*) FROM nav_history"))
    print(result.scalar())
    
    print("\n--- Sample NAV History ---")
    df_nav = pd.read_sql(text("SELECT * FROM nav_history LIMIT 5"), conn)
    print(df_nav)
