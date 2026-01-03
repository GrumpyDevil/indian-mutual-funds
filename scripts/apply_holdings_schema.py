import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection
from sqlalchemy import text
import os
import logging

logging.basicConfig(level=logging.INFO)

def apply_schema():
    engine = get_db_connection()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to find sql/holdings_schema.sql from scripts/
    schema_path = os.path.join(base_dir, '..', 'sql', 'holdings_schema.sql')
    
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            sql = f.read()
            
        with engine.begin() as conn:
            conn.execute(text(sql))
        logging.info("Holdings schema applied.")
    else:
        logging.error(f"Schema file not found at {schema_path}")

if __name__ == "__main__":
    apply_schema()
