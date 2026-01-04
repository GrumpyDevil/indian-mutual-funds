import pandas as pd
file_path = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')
# Let's filter for one fund that had a negative total in my previous run
fund = "ICICI Prudential Dynamic Asset Allocation Active FoF Direct Growth"
print(f"Transactions for {fund}:")
print(df[df['Scheme Name'] == fund][['Date', 'Transaction Type', 'Units', 'Actual Amount']])
print("\nSum of Actual Amount:", df[df['Scheme Name'] == fund]['Actual Amount'].sum())
print("Sum of Units:", df[df['Scheme Name'] == fund]['Units'].sum())
