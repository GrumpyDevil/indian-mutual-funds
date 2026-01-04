import pandas as pd

def parse_cams(tables):
    """
    Parses CAMS format tables into a list of holdings.
    """
    holdings = []

    for df in tables:
        if df.empty or len(df) < 2:
            continue
            
        # Clean columns: handle cases where header might be on multiple rows
        df.columns = df.iloc[0]
        df = df[1:]

        if "Scheme Name" not in df.columns:
            continue

        for _, row in df.iterrows():
            try:
                # Basic cleaning of units and values
                units_str = str(row.get("Unit Balance", "0")).replace(",", "")
                nav_str = str(row.get("NAV", "0")).replace(",", "")
                value_str = str(row.get("Market Value", "0")).replace(",", "")
                
                holdings.append({
                    "amc": row.get("AMC Name", ""),
                    "scheme": row.get("Scheme Name", ""),
                    "folio": row.get("Folio No", ""),
                    "units": float(units_str) if units_str else 0.0,
                    "nav": float(nav_str) if nav_str else 0.0,
                    "value": float(value_str) if value_str else 0.0
                })
            except (ValueError, TypeError):
                continue

    return holdings
