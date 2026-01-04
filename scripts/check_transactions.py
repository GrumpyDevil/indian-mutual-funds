import pandas as pd
import os

file_path = r'c:\Users\aryan\Codes\indian-mutual-funds\data\MF Transactions.xlsx'
if os.path.exists(file_path):
    xl = pd.ExcelFile(file_path)
    print("Sheets:", xl.sheet_names)
    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"\nSheet: {sheet}")
        print("Columns:", df.columns.tolist())
        print(df.head(10))
else:
    print(f"File not found: {file_path}")
