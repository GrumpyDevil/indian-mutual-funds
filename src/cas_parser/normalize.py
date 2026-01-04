def normalize(holdings):
    """
    Normalizes different parser outputs to a standard schema.
    """
    norm = []

    for h in holdings:
        norm.append({
            "amc": h.get("amc", ""),
            "scheme": h.get("scheme", ""),
            "folio": h.get("folio", ""),
            "units": round(float(h.get("units", 0)), 4),
            "nav": round(float(h.get("nav", 0)), 4),
            "value": round(float(h.get("value", 0)), 2)
        })

    return norm
