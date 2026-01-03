import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'mutualfunds')

connection_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_str)

def check():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT count(*) FROM portfolio_holdings")).scalar()
        print(f"Total Holdings: {res}")
        if res > 0:
            df = pd.read_sql(text("SELECT company_name, percentage_holding FROM portfolio_holdings WHERE company_name IS NOT NULL LIMIT 10"), conn)
            print("\nTop 10 Holdings sample:")
            print(df.to_string())

if __name__ == "__main__":
    check()
