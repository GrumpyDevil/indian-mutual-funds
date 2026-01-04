from mftool import Mftool
mf = Mftool()
all_codes = mf.get_scheme_codes()
for code, name in all_codes.items():
    if "Momentum 30" in name:
        print(f"{code}: {name}")
