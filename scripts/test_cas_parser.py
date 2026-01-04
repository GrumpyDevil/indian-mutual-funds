import sys
import os
import getpass
from src.cas_parser.main import parse_cas

def main():
    if len(sys.argv) < 2:
        pdf_path = input("Enter path to CAS PDF: ")
    else:
        pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    pan = input("Enter PAN (default will be used if empty): ")
    dob = input("Enter DOB in DDMMYYYY format: ")

    try:
        print(f"Parsing {pdf_path}...")
        result = parse_cas(pdf_path, pan, dob)
        
        print("\n" + "="*50)
        print(f"CAS Type: {result['type']}")
        print(f"Found {len(result['holdings'])} valid holdings.")
        print("="*50)
        
        for h in result['holdings']:
            print(f"- {h['scheme']}")
            print(f"  Units: {h['units']}, NAV: {h['nav']}, Value: {h['value']}")
            
        if result['errors']:
            print("\nErrors:")
            for err in result['errors']:
                print(f"! {err}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Add project root to sys.path
    sys.path.append(os.getcwd())
    main()
