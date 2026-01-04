from pypdf import PdfReader

def decrypt_pdf(path, pan=None, dob_ddmmyyyy=None):
    """
    Decrypts a password-protected CAS PDF if needed.
    Password prefix (usually): PAN (UPPERCASE) + DOB (DDMMYYYY)
    """
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            if not pan or not dob_ddmmyyyy:
                raise Exception("PDF is encrypted but PAN or DOB not provided.")
            password = pan.upper() + dob_ddmmyyyy
            reader.decrypt(password)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            # Fallback to pdfplumber if pypdf returns empty text
            import pdfplumber
            with pdfplumber.open(path, password=(pan.upper() + dob_ddmmyyyy) if reader.is_encrypted else None) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

        if not text.strip():
            raise Exception("PDF contains no extractable text.")

        return reader, text
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")
