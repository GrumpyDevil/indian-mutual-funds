import os
import json
from mftool import Mftool
import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Uses environment variables for credentials, defaults to localhost/postgres.
    """
    import urllib.parse
    from dotenv import load_dotenv
    load_dotenv()
    
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'mutualfunds')

    encoded_password = urllib.parse.quote_plus(db_password)
    connection_str = f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_str)
    return engine

def init_db(engine):
    """
    Initializes the database by running the schema.sql file.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, '..', 'sql', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        with engine.begin() as conn:
            conn.execute(text(schema_sql))
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise

def sync_schemes(engine):
    """
    Fetches all available schemes from mftool and updates the 'schemes' table.
    """
    mf = Mftool()
    logging.info("Fetching all scheme codes from mftool...")
    scheme_codes = mf.get_scheme_codes() # Returns a dictionary {code: name}
    
    # Prepare data for insertion
    data = []
    for code, name in scheme_codes.items():
        data.append({'scheme_code': str(code), 'scheme_name': name})
    
    df = pd.DataFrame(data)
    
    logging.info(f"Found {len(df)} schemes. Syncing to database...")
    
    # We use 'to_sql' with method='multi' for bulk insert, but we need to handle upserts.
    # For simplicity in this step, we will use a naive approach: insert ignore or simple insert.
    # Since pandas 'replace' drops the table, and 'append' might fail on duplicates with PK,
    # let's do a more careful upsert manually or catch errors. 
    # For now, let's just insert new ones (safely) or replace if the user wants full refresh.
    # Actually, let's use a raw SQL query for upsert (ON CONFLICT DO NOTHING) to be safe and efficient.
    
    with engine.begin() as conn:
        # Create a temporary table
        df.to_sql('temp_schemes', conn, if_exists='replace', index=False)
        
        # Upsert from temp table to main table
        upsert_query = text("""
            INSERT INTO schemes (scheme_code, scheme_name)
            SELECT scheme_code, scheme_name FROM temp_schemes
            ON CONFLICT (scheme_code) DO UPDATE 
            SET scheme_name = EXCLUDED.scheme_name,
                last_updated = CURRENT_TIMESTAMP;
        """)
        conn.execute(upsert_query)
        
        # Drop temp table
        conn.execute(text("DROP TABLE temp_schemes"))

    logging.info("Schemes synced successfully.")

def fetch_nav_history(engine, scheme_code):
    """
    Fetches historical NAV for a given scheme and stores it.
    Attempts to fetch full history if possible.
    """
    mf = Mftool()
    logging.info(f"Fetching NAV history for scheme: {scheme_code}")
    
    # Check if we already have data to decide on partial or full update
    # For this implementation, we will always try to fetch full history 
    # but rely on database 'ON CONFLICT' to ignore duplicates.
    # mftool's get_scheme_historical_nav fetches data since inception if no dates provided (usually).
    # However, let's explicitely ask for a large range or check docs.
    # The default behaviour often gets last few years or all.
    # Validated: get_scheme_historical_nav(code, as_Dataframe=True) returns all available history.
    
    try:
        data = mf.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
    except Exception as e:
        logging.error(f"Error fetching data for {scheme_code}: {e}")
        return

    if data is not None and not data.empty:
        # Cleanup data
        # Data often has date as index
        if 'date' not in data.columns and data.index.name == 'date':
             data = data.reset_index()

        if 'date' in data.columns and 'nav' in data.columns:
            if data.index.name == 'date':
                data = data.reset_index()
                
            data['nav_date'] = pd.to_datetime(data['date'], dayfirst=True)
            data['nav_value'] = pd.to_numeric(data['nav'], errors='coerce')
            data['scheme_code'] = scheme_code
            
            # Select relevant columns
            df_to_insert = data[['scheme_code', 'nav_date', 'nav_value']].dropna()
            
            if df_to_insert.empty:
                 logging.warning(f"No valid data to insert for {scheme_code}")
                 return

            # Insert into DB
            with engine.begin() as conn:
                 # Create temp table
                df_to_insert.to_sql('temp_nav', conn, if_exists='replace', index=False)
                
                # Upsert
                upsert_query = text("""
                    INSERT INTO nav_history (scheme_code, nav_date, nav_value)
                    SELECT scheme_code, nav_date, nav_value FROM temp_nav
                    ON CONFLICT (scheme_code, nav_date) DO NOTHING;
                """)
                conn.execute(upsert_query)
                conn.execute(text("DROP TABLE temp_nav"))

            logging.info(f"Inserted/Updated {len(df_to_insert)} NAV records for {scheme_code}")
        else:
            # Sometimes data comes in different format or empty list
            logging.warning(f"Unexpected data format for {scheme_code}: {data.columns if hasattr(data, 'columns') else data}")

    else:
        logging.info(f"No new data found for scheme {scheme_code}")

if __name__ == "__main__":
    
    # 1. Connect
    try:
        engine = get_db_connection()
        logging.info("Connected to database.")
    except Exception as e:
        logging.error(f"Failed to connect to DB: {e}")
        exit(1)

    # 2. Init DB (Create tables)
    init_db(engine)

    # 3. Sync Schemes (Run this once or periodically)
    sync_schemes(engine)

    # 4. Fetch NAV for ALL schemes
    # Get all scheme codes from DB
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT scheme_code FROM schemes"))
            all_codes = [row[0] for row in result.fetchall()]
    except Exception as e:
        logging.error(f"Failed to fetch scheme codes: {e}")
        exit(1)

    import concurrent.futures

    logging.info(f"Starting fetch for {len(all_codes)} schemes...")
    
    # Use ThreadPoolExecutor for parallel IO. 
    # Be careful with rate limits. AMFI might block if too aggressive.
    # Start gentle: 5 workers.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_code = {executor.submit(fetch_nav_history, engine, code): code for code in all_codes}
        
        for future in concurrent.futures.as_completed(future_to_code):
            code = future_to_code[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Exception for {code}: {e}")

    logging.info("Done.")
