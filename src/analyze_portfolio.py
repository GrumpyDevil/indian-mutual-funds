import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings

from .finance import safe_xirr, calculate_cagr, aggregate_units, get_market_value
from .benchmark import simulate_benchmark_sip
from .data_manager import DataManager
from .cas_parser.main import parse_cas

warnings.filterwarnings('ignore')

# Constants
TRANSACTIONS_FILE = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
CAS_PDF_FILE = r'c:\Users\aryan\Codes\indian-mutual-funds\data\NSDL-Consolidated Account Statement.pdf'
NIFTY_50_TICKER = "^NSEI"
NIFTY_TRI_SCHEME_CODE = "120716" # UTI Nifty 50 Index Fund - Direct - Growth

# Manual Overrides for known tricky names
MANUAL_MAPPING = {
    "HSBC Midcap Fund Growth": "151036",
    "Canara Robeco Large and Mid Cap Fund Growth": "118278",
    "Nippon India Small Cap Fund Direct Growth": "118778",
    "Franklin U.S. Opportunities Equity Active FoF Direct Growth": "118551",
    "UTI Nifty200 Momentum 30 Index Fund Direct Growth": "148703",
    "Quant Mid Cap Fund Direct Growth": "120841",
    "Quant Small Cap Fund Direct Plan Growth": "120828",
    "Quant Multi Cap Fund Direct Growth": "120823",
    "Motilal Oswal Nifty Microcap 250 Index Fund Direct Growth": "151814",
    "Parag Parikh Flexi Cap Fund Direct Growth": "122639",
    "ICICI Prudential Liquid Fund Direct Plan Growth": "120197",
    "Nippon India Liquid Fund Direct Growth": "118701",
    "SBI Small Cap Fund Direct Growth": "125497",
    "ICICI Prudential Technology Direct Plan Growth": "120594",
    "ICICI Prudential Dynamic Asset Allocation Active FoF Direct Growth": "120679"
}

def main():
    dm = DataManager(manual_mapping=MANUAL_MAPPING)
    
    # Check if we should use CAS PDF
    cas_holdings = {}
    if os.path.exists(CAS_PDF_FILE):
        print(f"Loading CAS data from {CAS_PDF_FILE}...")
        try:
            res = parse_cas(CAS_PDF_FILE)
            print(f"  Successfully parsed {res['type']} CAS with {len(res['holdings'])} holdings.")
            for h in res['holdings']:
                cas_holdings[h['scheme']] = h
        except Exception as e:
            print(f"  Note: CAS parsing failed: {e}")

    # 1. Load Transactions
    print(f"Loading transactions from {TRANSACTIONS_FILE}...")
    df = pd.read_excel(TRANSACTIONS_FILE, sheet_name='Sheet1')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # 2. Fix Signs and Units
    df['Effective Units'] = df['Units'].abs() * np.sign(df['Actual Amount'])
    
    # 3. Map schemes
    unique_schemes = df['Scheme Name'].unique()
    scheme_mapping = {}
    print("Mapping scheme names to codes...")
    for s in unique_schemes:
        code = dm.find_best_match(s)
        if code:
            scheme_mapping[s] = code
            print(f"  Matched: '{s}' -> {code}")
        else:
            print(f"  FAILED to match: '{s}'")
    
    # 4. Fetch NAVs
    current_navs = {}
    print("Fetching current NAVs...")
    for s, code in scheme_mapping.items():
        current_navs[s] = dm.fetch_current_nav(code)

    # 5. Benchmark Data
    print("Fetching benchmark data...")
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    nifty50_nav = dm.fetch_index_data(NIFTY_50_TICKER, start_date)
    nifty_tri_nav = dm.fetch_historical_nav(NIFTY_TRI_SCHEME_CODE)
    
    # 6. Calculations
    today = datetime.now()
    portfolio_cfs = [] 
    for _, row in df.iterrows():
        portfolio_cfs.append((row['Date'], -row['Actual Amount']))
        
    # Portfolio current value
    current_portfolio_value = 0
    fund_details = []
    for s in unique_schemes:
        units = aggregate_units(df, s)
        invested_in_fund = df[df['Scheme Name'] == s]['Actual Amount'].sum()
        curr_nav = current_navs.get(s, 0)
        curr_val = get_market_value(units, curr_nav)
        
        current_portfolio_value += curr_val
        if abs(units) > 0.001 or abs(invested_in_fund) > 1:
            fund_details.append({
                'Scheme': (s[:35] + '..') if len(s) > 37 else s,
                'Net Capital': invested_in_fund,
                'Units': units,
                'Value': curr_val,
                'Ret%': (curr_val / invested_in_fund - 1) * 100 if invested_in_fund > 0 else 0
            })
    
    portfolio_cfs.append((today, current_portfolio_value))
    xirr_port = safe_xirr(portfolio_cfs)
    
    # Benchmark Simulations
    _, val_50, xirr_50, _ = simulate_benchmark_sip(df, nifty50_nav, today)
    _, val_tri, xirr_tri, _ = simulate_benchmark_sip(df, nifty_tri_nav, today)
    
    net_capital_invested = df['Actual Amount'].sum()
    total_purchase = df[df['Actual Amount'] > 0]['Actual Amount'].sum()
    total_redemption = df[df['Actual Amount'] < 0]['Actual Amount'].abs().sum()
    
    # 7. Report
    print("\n" + "="*80)
    print(f" PORTFOLIO PERFORMANCE SUMMARY (As of {today.strftime('%d-%b-%Y')})")
    print("="*80)
    print(f"{'Metric':<30} | {'Portfolio':<14} | {'Nifty 50':<14} | {'Nifty 50 TRI':<14}")
    print("-" * 80)
    
    def fmt_pct(val):
        return f"{val*100:>.2f}%" if val is not None else "N/A"
    def fmt_amt(val):
        return f"{val:,.0f}"

    print(f"{'XIRR (Annualized)':<30} | {fmt_pct(xirr_port):<14} | {fmt_pct(xirr_50):<14} | {fmt_pct(xirr_tri):<14}")
    print(f"{'Current Portfolio Value':<30} | {fmt_amt(current_portfolio_value):<14} | {fmt_amt(val_50):<14} | {fmt_amt(val_tri):<14}")
    print(f"{'Net Capital Invested':<30} | {fmt_amt(net_capital_invested):<14} | {fmt_amt(net_capital_invested):<14} | {fmt_amt(net_capital_invested):<14}")
    print(f"{'Total Profit/Loss':<30} | {fmt_amt(current_portfolio_value - net_capital_invested):<14} | {fmt_amt(val_50 - net_capital_invested):<14} | {fmt_amt(val_tri - net_capital_invested):<14}")
    print("-" * 80)
    print(f"{'Gross Investment (Purchases)':<30} | {fmt_amt(total_purchase):<14}")
    print(f"{'Gross Redemptions (Sales)':<30} | {fmt_amt(total_redemption):<14}")
    print("="*80)
    
    print("\nINDIVIDUAL FUND BREAKDOWN:")
    fund_df = pd.DataFrame(fund_details)
    if not fund_df.empty:
        print(fund_df[['Scheme', 'Units', 'Net Capital', 'Value', 'Ret%']].to_string(index=False))

    if cas_holdings:
        print("\nCAS HOLDINGS (for verification):")
        for s, h in cas_holdings.items():
            print(f"  {s[:50]:<50} | Units: {h['units']:>10.4f} | Value: {h['value']:>12,.2f}")

if __name__ == "__main__":
    main()
