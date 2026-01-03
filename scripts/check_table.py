from src.fetch_data import get_db_connection
from sqlalchemy import text

engine = get_db_connection()
with engine.connect() as conn:
    res = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'portfolio_holdings'"))
    for row in res.fetchall():
        print(row)
