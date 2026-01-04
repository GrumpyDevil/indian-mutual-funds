import pandas as pd

def parse_kfintech(tables):
    """
    Parses KFintech format tables into a list of holdings.
    """
    holdings = []

    for df in tables:
        if df.empty or len(df) < 2:
            continue
            
        df.columns = df.iloc[0]
        df = df[1:]

        if "Scheme" not in df.columns:
            continue

        for _, row in df.iterrows():
            try:
                units_str = str(row.get("Closing Units", "0")).replace(",", "")
                nav_str = str(row.get("NAV", "0")).replace(",", "")
                value_str = str(row.get("Value", "0")).replace(",", "")
                
                holdings.append({
                    "amc": row.get("Fund House", ""),
                    "scheme": row.get("Scheme", ""),
                    "folio": row.get("Folio Number", ""),
                    "units": float(units_str) if units_str else 0.0,
                    "nav": float(nav_str) if nav_str else 0.0,
                    "value": float(value_str) if value_str else 0.0
                })
            except (ValueError, TypeError):
                continue

    return holdings
