import pandas as pd
file_path = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')
unique_schemes = df['Scheme Name'].unique().tolist()
for s in unique_schemes:
    print(s)
