from src.fetch_data import get_db_connection
from sqlalchemy import text

engine = get_db_connection()
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE portfolio_holdings"))
    conn.execute(text("ALTER TABLE portfolio_holdings DROP CONSTRAINT IF EXISTS portfolio_holdings_scheme_code_company_name_date_reported_key"))
    # Use id as the tiebreaker if company_name/isin/date match (unlikely but safe)
    # Actually, let's just use NO unique constraint for now and rely on DELETE before INSERT.
    # It's much simpler for various AMC formats.
    print("Table truncated and constraint dropped.")
