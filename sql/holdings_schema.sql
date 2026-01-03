-- Table to store Portfolio Holdings
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id SERIAL PRIMARY KEY,
    scheme_code VARCHAR(50) REFERENCES schemes(scheme_code),
    company_name TEXT,
    sector TEXT,
    nature TEXT,
    -- e.g., 'EQ' for Equity, 'DEBT' for Debt
    quantity DECIMAL(20, 4),
    market_value DECIMAL(20, 2),
    percentage_holding DECIMAL(5, 2),
    date_reported DATE,
    market_cap_class VARCHAR(50),
    -- e.g., 'Large Cap', 'Mid Cap'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scheme_code, company_name, date_reported)
);
-- Index for querying holdings overlaps
CREATE INDEX IF NOT EXISTS idx_holdings_company ON portfolio_holdings(company_name);
CREATE INDEX IF NOT EXISTS idx_holdings_scheme_date ON portfolio_holdings(scheme_code, date_reported);