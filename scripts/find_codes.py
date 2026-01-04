from mftool import Mftool
import json

mf = Mftool()
all_codes = mf.get_scheme_codes()

keywords = [
    "UTI Nifty200 Momentum 30",
    "Canara Robeco Large and Mid",
    "Nippon India Small Cap",
    "Franklin U.S. Opportunities",
    "HSBC Midcap",
    "Microcap",
    "Quant Mid Cap"
]

results = {}
for code, name in all_codes.items():
    for kw in keywords:
        if kw.lower() in name.lower():
            if kw not in results: results[kw] = []
            results[kw].append(f"{code}: {name}")

for kw, matches in results.items():
    print(f"\nMatches for '{kw}':")
    for m in matches:
        print(f"  {m}")
