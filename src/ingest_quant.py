import pandas as pd
import os
import sys
import logging
import re
from sqlalchemy import text
from datetime import datetime

# Adjust path to find src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_data import get_db_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_scheme_code_by_name(engine, name):
    """
    Tries to find the most likely scheme_code for a given scheme name.
    """
    # Simple direct match first
    with engine.connect() as conn:
        # Search for exact or fuzzy match
        # Often the name in Excel misses "Direct Plan" or "Regular Plan"
        search_name = name.strip()
        query = text("SELECT scheme_code FROM schemes WHERE scheme_name ILIKE :name LIMIT 1")
        res = conn.execute(query, {"name": f"%{search_name}%"})
        row = res.fetchone()
        if row:
            return row[0]
        
        # Try a more relaxed search if direct fails
        # e.g. "quant Large Cap Fund" -> "quant Large Cap Fund%"
        query = text("SELECT scheme_code FROM schemes WHERE scheme_name ILIKE :name LIMIT 1")
        res = conn.execute(query, {"name": f"{search_name}%"})
        row = res.fetchone()
        if row:
            return row[0]

    return None

def parse_quant_sheet(engine, excel_path, sheet_name):
    try:
        # Read the sheet without header first to find the data table
        df_raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
        
        if df_raw.empty:
            return

        # 1. Detect Scheme Name
        scheme_name_raw = None
        header_row_idx = -1
        
        # Search for scheme name and header row simultaneously
        for i, row in df_raw.head(20).iterrows():
            row_vals = [str(x).strip().lower() for x in row.values]
            
            # Look for scheme name
            if not scheme_name_raw:
                for val in row.values:
                    v = str(val).strip()
                    if "fund" in v.lower() and "quant" in v.lower() and v.lower() != "quant mutual fund":
                        scheme_name_raw = v
            
            # Look for header row (contains ISIN)
            if "isin" in row_vals:
                header_row_idx = i
                
        if not scheme_name_raw:
            logging.warning(f"Could not find scheme name in sheet {sheet_name}. Skipping.")
            return
            
        logging.info(f"Detected scheme name: {scheme_name_raw} (from sheet {sheet_name})")
        
        scheme_code = get_scheme_code_by_name(engine, scheme_name_raw)
        if not scheme_code:
            logging.warning(f"Could not match '{scheme_name_raw}' to any scheme code in DB. Skipping.")
            return

        # 2. Extract Data Table
        if header_row_idx == -1:
            logging.warning(f"Could not find header row (with 'ISIN') in sheet {sheet_name}. Skipping.")
            return
            
        # Set columns from the header row
        df = df_raw.iloc[header_row_idx+1:].copy()
        cols = [str(x).strip() for x in df_raw.iloc[header_row_idx].values]
        df.columns = cols
        
        # 3. Detect Report Date
        # Usually in the row above the header or a few rows up
        report_date = datetime.now().date()
        date_pattern = r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})'
        for i in range(max(0, header_row_idx-5), header_row_idx):
            row_str = " ".join([str(x) for x in df_raw.iloc[i].values])
            date_match = re.search(date_pattern, row_str)
            if date_match:
                try:
                    report_date = datetime.strptime(date_match.group(1), '%d %b %Y').date()
                    break
                except:
                    pass
        
        logging.info(f"Raw Columns from header row: {cols}")

        df.columns = cols
        
        # 3. Detect Report Date
        report_date = datetime.now().date()
        date_pattern = r'(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})' # Dec 2025
        for i in range(max(0, header_row_idx-5), header_row_idx):
            row_str = " ".join([str(x) for x in df_raw.iloc[i].values])
            date_match = re.search(date_pattern, row_str, re.IGNORECASE)
            if date_match:
                try:
                    # Try Dec, Nov etc
                    report_date = datetime.strptime(date_match.group(1), '%d %b %Y').date()
                    break
                except:
                    pass
        
        logging.info(f"Report date detected: {report_date}")

        # Ensure columns are unique and clean
        df.columns = [str(c).strip() for c in df.columns]

        # 4. Normalize and Clean
        mapping = {
            'ISIN': 'isin',
            'NAME OF THE INSTRUMENT': 'company_name',
            'INDUSTRY': 'sector',
            'QUANTITY': 'quantity',
            'MARKET VALUE (RS. LAKHS)': 'market_value',
            'MARKET VALUE(Rs.in Lakhs)': 'market_value',
            '% to NAV': 'percentage_holding',
            '% TO NAV': 'percentage_holding'
        }
        df = df.rename(columns=mapping)
        
        # Keep only relevant columns
        db_cols = ['isin', 'company_name', 'sector', 'quantity', 'market_value', 'percentage_holding']
        available = [c for c in db_cols if c in df.columns]
        df = df[available].copy()
        
        logging.info(f"Data columns: {df.columns.tolist()}")
        
        # Data cleaning
        df = df.dropna(subset=['isin', 'company_name'])
        df['isin'] = df['isin'].astype(str).str.strip().str.upper()
        df['company_name'] = df['company_name'].astype(str).str.strip()
        
        # Filter for valid ISINs
        df = df[df['isin'].str.startswith('IN')]
        df = df[df['isin'].str.len() >= 12]
        
        # IMPORTANT: Quant sheet has "Short" / "Long" rows that might have the same ISIN
        # as the main row (it's a breakdown). We should probably sum them or pick one.
        # For simplicity, we'll keep the first one or sum if they are duplicates.
        # But usually we just want the net position.
        
        if df.empty:
            logging.warning(f"No valid holdings found after filtering in sheet {sheet_name}.")
            return

        df['scheme_code'] = scheme_code
        df['date_reported'] = report_date
        
        # Clean numeric cols
        for col in ['quantity', 'market_value', 'percentage_holding']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Ensure no NaN remains in text columns
        df['sector'] = df['sector'].fillna('Unknown')

        records = df.to_dict(orient='records')
        logging.info(f"Inserting {len(records)} records for {scheme_name_raw}")
        if records:
             logging.info(f"First record: {records[0]}")

        with engine.begin() as conn:
            # 1. DROP the unique constraint if it exists to prevent 'already exists' errors
            # We will rely on deleting by (scheme, date) before insert
            conn.execute(text("ALTER TABLE portfolio_holdings DROP CONSTRAINT IF EXISTS portfolio_holdings_scheme_code_company_name_date_reported_key"))
            
            # 2. Delete existing records for this scheme/date to allow clean re-ingest
            conn.execute(text("DELETE FROM portfolio_holdings WHERE scheme_code = :s AND date_reported = :d"), 
                         {"s": scheme_code, "d": report_date})
            
            if records:
                # 3. Bulk insert using sqlalchemy core
                from sqlalchemy import insert
                from sqlalchemy.schema import Table, MetaData
                metadata = MetaData()
                table = Table('portfolio_holdings', metadata, autoload_with=engine)
                conn.execute(insert(table), records)
            
        logging.info(f"Successfully ingested {len(df)} holdings for {scheme_name_raw} ({scheme_code})")

    except Exception as e:
        logging.error(f"Error parsing sheet {sheet_name}: {e}")

def main():
    excel_path = "data/holdings_excel/quant_MF_Monthly_Portfolio_Nov_2025.xlsx"
    if not os.path.exists(excel_path):
        logging.error(f"File not found: {excel_path}")
        return

    engine = get_db_connection()
    xl = pd.ExcelFile(excel_path)
    
    logging.info(f"Sheets found: {xl.sheet_names}")
    
    # Ingest sheets. For testing, we can limit to first 3 or specific ones.
    # qMES = Equity Savings, qActive = Active Fund
    test_sheets = [s for s in xl.sheet_names if s in ['qMES', 'qActive', 'qVF', 'qMMO']]
    if not test_sheets:
        test_sheets = xl.sheet_names[:5]

    for sheet in test_sheets:
        logging.info(f"--- Processing Sheet: {sheet} ---")
        parse_quant_sheet(engine, excel_path, sheet)

if __name__ == "__main__":
    main()
