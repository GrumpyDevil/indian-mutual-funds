import pandas as pd
file_path = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Check consistency of sign between Actual Amount and Units
# Let's count how many rows have same sign vs different signs
df['Sign_Amount'] = df['Actual Amount'].apply(lambda x: 1 if x >= 0 else -1)
df['Sign_Units'] = df['Units'].apply(lambda x: 1 if x >= 0 else -1)

mismatches = df[df['Sign_Amount'] != df['Sign_Units']]
print(f"Total rows: {len(df)}")
print(f"Mismatches in sign: {len(mismatches)}")
if len(mismatches) > 0:
    print("\nFirst 10 mismatches:")
    print(mismatches[['Scheme Name', 'Transaction Type', 'Units', 'Actual Amount', 'Sign_Amount', 'Sign_Units']].head(10))
