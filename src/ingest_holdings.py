import pandas as pd
import os
import sys
import logging
from sqlalchemy import text
from datetime import datetime

# Adjust path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection

logging.basicConfig(level=logging.INFO)

def normalize_columns(df):
    """
    Normalize column names to find standard fields.
    """
    df.columns = df.columns.str.strip().str.lower()
    mapping = {
        'isin': 'isin',
        'name of the instrument': 'company_name',
        'company name': 'company_name',
        'name of the security': 'company_name',
        'industry': 'sector',
        'sector': 'sector',
        'market value': 'market_value',
        'market value (rs. lakhs)': 'market_value',
        '% to nav': 'percentage_holding',
        '% of aum': 'percentage_holding',
        'quantity': 'quantity',
        'units': 'quantity'
        # Add more mappings as discovered
    }
    return df.rename(columns=mapping)

def ingest_excel(file_path):
    engine = get_db_connection()
    try:
        logging.info(f"Processing {file_path}")
        # Read Excel - often data starts after some header rows. 
        # We might need to inspect or try multiple skip_rows.
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
             logging.error(f"Failed to read excel {file_path}: {e}")
             return

        # Simple heuristic: find the row with 'ISIN' or 'Name'
        header_row = -1
        for i, row in df.head(20).iterrows():
            row_str = row.astype(str).str.lower().values
            if 'isin' in row_str or 'company name' in row_str or 'name of the instrument' in row_str:
                header_row = i
                break
        
        if header_row != -1:
            df = pd.read_excel(file_path, skiprows=header_row+1)
            # Re-read with correct header. Actually skiprows=header_row usually makes that row the header.
            # Let's do header=header_row
            df = pd.read_excel(file_path, header=header_row)
        
        df = normalize_columns(df)
        
        required_cols = ['company_name', 'percentage_holding'] # Minimal required
        if not all(col in df.columns for col in required_cols):
             logging.warning(f"Skipping {file_path}: Missing required columns. Found: {df.columns}")
             return

        # NEED: Scheme Code. This is hard. It might be in the filename or a cell in the first few rows.
        # For this prototype, let's assume filename contains scheme code or name we can fuzzy match.
        # OR: We just assume user provides it or we parse it.
        # Let's rely on filename having the scheme code for now (e.g., "120503_portfolio.xlsx")
        
        filename = os.path.basename(file_path)
        # Try to extract scheme code (digits)
        import re
        match = re.search(r'(\d{6})', filename)
        if match:
            scheme_code = match.group(1)
        else:
            logging.warning(f"Could not extract scheme code from filename {filename}. Skipping.")
            return

        # Clean data
        df = df[df['company_name'].notna()]
        
        # Prepare for DB
        records = []
        date_reported = datetime.now().date() # Limit: Don't know actual date report from Excel yet.
        
        # Try finding date in first few rows of original file?
        # For now, use today or file mod time.
        
        for _, row in df.iterrows():
            record = {
                'scheme_code': scheme_code,
                'company_name': row.get('company_name'),
                'sector': row.get('sector'),
                'quantity': row.get('quantity') if pd.notna(row.get('quantity')) else 0,
                'percentage_holding': row.get('percentage_holding') if pd.notna(row.get('percentage_holding')) else 0,
                'date_reported': date_reported # Placeholder
            }
            records.append(record)
            
        if not records:
             return

        df_db = pd.DataFrame(records)
        
        with engine.begin() as conn:
             # Upsert logic (simplified insert for now)
             # delete old for this scheme/date? OR on conflict
             # Let's delete for this scheme+date to allow re-ingest
             conn.execute(text("DELETE FROM portfolio_holdings WHERE scheme_code = :s AND date_reported = :d"), 
                          {"s": scheme_code, "d": date_reported})
             
             df_db.to_sql('portfolio_holdings', conn, if_exists='append', index=False, chunksize=1000)
             
        logging.info(f"Ingested {len(df_db)} records for {scheme_code}")

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

def main():
    folder = "data/holdings_excel"
    if not os.path.exists(folder):
        os.makedirs(folder)
        logging.info(f"Created {folder}. Put .xlsx files there.")
        return

    for file in os.listdir(folder):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            ingest_excel(os.path.join(folder, file))

if __name__ == "__main__":
    main()
