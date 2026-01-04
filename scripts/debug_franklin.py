import pandas as pd
file_path = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')
fund = "Franklin U.S. Opportunities Equity Active FoF Direct Growth"
print(f"Transactions for {fund}:")
print(df[df['Scheme Name'] == fund][['Date', 'Units', 'Actual Amount', 'NAV']])
