from src.fetch_data import get_db_connection
from sqlalchemy import text
engine = get_db_connection()
with engine.connect() as conn:
    count = conn.execute(text("SELECT count(*) FROM portfolio_holdings")).scalar()
    print(f"Total Holdings: {count}")
    
    sample = conn.execute(text("SELECT * FROM portfolio_holdings LIMIT 5")).fetchall()
    print("\nSample records:")
    for s in sample:
        print(s)
