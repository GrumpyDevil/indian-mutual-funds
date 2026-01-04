def detect_cas_type(text):
    """
    Detects the CAS provider type based on the extracted text.
    """
    t = text.upper()

    # Prioritize NSDL/CDSL for these types of statements
    if "NATIONAL SECURITIES DEPOSITORY" in t or "NSDL CAS" in t:
        return "NSDL"
    if "CENTRAL DEPOSITORY SERVICES" in t or "CDSL CAS" in t:
        return "CDSL"
    if "COMPUTER AGE MANAGEMENT SERVICES" in t or "CAMS" in t:
        return "CAMS"
    if "KFIN TECHNOLOGIES" in t or "KARVY" in t:
        return "KFINTECH"

    raise Exception("Unknown CAS format")
