import yfinance as yf
import pandas as pd

tickers = ["^NSEI", "^NSEBANK", "NIFTY_50.NS", "0P0000XWWI.BO"]
for ticker in tickers:
    try:
        data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        if not data.empty:
            print(f"Ticker {ticker} found. Latest price: {data['Close'].iloc[-1]}")
        else:
            print(f"Ticker {ticker} returned empty data.")
    except Exception as e:
        print(f"Ticker {ticker} error: {e}")
