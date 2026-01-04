import re

def parse_nsdl(text):
    """
    Parses NSDL format text into a list of holdings using regex.
    Supports both block format and tabular format.
    """
    holdings = []
    
    # 1. Block format (from code.txt)
    block_pattern = re.compile(
        r"Scheme Name\s*:\s*(.+?)\n.*?"
        r"Units\s*:\s*([\d\.]+).*?"
        r"NAV\s*:\s*([\d\.]+).*?"
        r"Value\s*:\s*([\d,\.]+)",
        re.S
    )
    
    for match in block_pattern.findall(text):
        try:
            holdings.append({
                "scheme": match[0].strip(),
                "units": float(match[1]),
                "nav": float(match[2]),
                "value": float(match[3].replace(",", ""))
            })
        except: continue

    # 2. Tabular format (seen in actual text extraction)
    # Pattern to match: [Scheme Name] [Units] [NAV] [Value]
    # Example: NAGEMENT LIMITED SCHEME C - TIER I 962.2624 29.9259 28,796.56
    tabular_pattern = re.compile(
        r"([A-Z\s\-]+?)\s+([\d,]+\.\d{2,4})\s+([\d,]+\.\d{2,4})\s+([\d,]+\.\d{2})",
        re.M
    )
    
    if not holdings:
        for match in tabular_pattern.findall(text):
            try:
                name = match[0].strip()
                # Clean up newlines and common header noise
                name = re.sub(r'^[A-Z\s\-]+\n', '', name)
                name = name.replace('\n', ' ').strip()
                
                # Skip if name is too short or doesn't look like a scheme
                if len(name) < 5 or any(kw in name for kw in ["TOTAL", "SUB TOTAL", "PAGE"]):
                    continue
                    
                holdings.append({
                    "scheme": name,
                    "units": float(match[1].replace(",", "")),
                    "nav": float(match[2].replace(",", "")),
                    "value": float(match[3].replace(",", ""))
                })
            except: continue

    return holdings
