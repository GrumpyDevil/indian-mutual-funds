from src.fetch_data import get_db_connection
from sqlalchemy import text

engine = get_db_connection()
with engine.begin() as conn:
    # Drop old constraint
    conn.execute(text("ALTER TABLE portfolio_holdings DROP CONSTRAINT IF EXISTS portfolio_holdings_scheme_code_company_name_date_reported_key"))
    # Add new, more specific constraint
    # Using COALESCE for isin to handle potential nulls in composite unique keys
    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_portfolio_holdings_unique ON portfolio_holdings (scheme_code, company_name, COALESCE(isin, ''), date_reported)"))
    print("Schema updated successfully.")
