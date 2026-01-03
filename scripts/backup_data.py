import sys
import os
import pandas as pd
from sqlalchemy import text
import logging

# Adjust path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection

logging.basicConfig(level=logging.INFO)

def backup():
    engine = get_db_connection()
    backup_dir = "data/backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    try:
        with engine.connect() as conn:
            logging.info("Backing up 'schemes' table...")
            schemes_df = pd.read_sql(text("SELECT * FROM schemes"), conn)
            schemes_df.to_csv(f"{backup_dir}/schemes_backup.csv", index=False)
            logging.info(f"Saved {len(schemes_df)} schemes.")

            logging.info("Backing up 'nav_history' table (using chunks)...")
            output_file = f"{backup_dir}/nav_history_backup.csv"
            
            # Start fresh or truncate
            if os.path.exists(output_file):
                os.remove(output_file)
                
            chunk_size = 500000 # 500k rows at a time
            first_chunk = True
            
            # Use connect for execution
            with engine.connect() as conn_read:
                # We need to use execution_options(stream_results=True) for postgres to stream
                # but pandas read_sql handles it if we pass chunksize.
                for df_chunk in pd.read_sql(text("SELECT * FROM nav_history"), conn_read, chunksize=chunk_size):
                    df_chunk.to_csv(output_file, mode='a', index=False, header=first_chunk)
                    first_chunk = False
                    logging.info(f"Appended chunk of {len(df_chunk)} rows...")
            
            logging.info("NAV history backup complete.")

    except Exception as e:
        logging.error(f"Backup failed: {e}")

if __name__ == "__main__":
    backup()
