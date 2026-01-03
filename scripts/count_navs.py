from src.fetch_data import get_db_connection
from sqlalchemy import text
engine = get_db_connection()
with engine.connect() as conn:
    count = conn.execute(text("SELECT count(*) FROM nav_history")).scalar()
    print(f"Total NAV records: {count}")
