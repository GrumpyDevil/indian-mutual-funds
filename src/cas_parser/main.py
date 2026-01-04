from .decrypt import decrypt_pdf
from .detect import detect_cas_type
from .extract_tables import extract_tables
from .parsers.cams import parse_cams
from .parsers.kfintech import parse_kfintech
from .parsers.nsdl import parse_nsdl
from .normalize import normalize
from .validate import validate

def parse_cas(pdf_path, pan=None, dob=None):
    """
    Main orchestrator to parse a CAS PDF.
    dob should be in DDMMYYYY format.
    """
    # 1. Decrypt and extract text
    reader, text = decrypt_pdf(pdf_path, pan, dob)
    
    # 2. Detect CAS type
    cas_type = detect_cas_type(text)
    
    # 3. Extract tables (for CAMS/KFintech)
    # Password might still be needed by camelot if it uses the original file
    password = (pan.upper() + dob) if (pan and dob) else None
    tables = extract_tables(pdf_path, password=password)
    
    # 4. Parse based on type
    data = []
    if cas_type == "CAMS":
        data = parse_cams(tables)
    elif cas_type == "KFINTECH":
        data = parse_kfintech(tables)
    elif cas_type == "NSDL":
        data = parse_nsdl(text)
    
    # 5. Normalize and Validate
    normalized_data = normalize(data)
    valid_data, errors = validate(normalized_data)
    
    return {
        "type": cas_type,
        "holdings": valid_data,
        "errors": errors
    }
