from mftool import Mftool
import pandas as pd

mf = Mftool()
d = mf.get_scheme_historical_nav("120716", as_Dataframe=True)
if d is not None:
    print(d.head())
else:
    print("Scheme not found")
