import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)

def reset_db():
    engine = get_db_connection()
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS nav_history CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS schemes CASCADE"))
    logging.info("Tables dropped.")

if __name__ == "__main__":
    reset_db()
