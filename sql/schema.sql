-- Table to store Mutual Fund Scheme details
CREATE TABLE IF NOT EXISTS schemes (
    scheme_code VARCHAR(50) PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    isin_growth VARCHAR(50),
    isin_reinvest VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Table to store Historical NAV data
CREATE TABLE IF NOT EXISTS nav_history (
    id SERIAL PRIMARY KEY,
    scheme_code VARCHAR(50) REFERENCES schemes(scheme_code),
    nav_date DATE,
    nav_value DECIMAL(15, 4),
    UNIQUE(scheme_code, nav_date)
);
-- Index for faster querying of NAVs by date and scheme
CREATE INDEX IF NOT EXISTS idx_nav_scheme_date ON nav_history(scheme_code, nav_date);