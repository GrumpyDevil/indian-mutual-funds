import camelot

def extract_tables(pdf_path, password=None):
    """
    Extracts tables from the PDF using camelot.
    """
    try:
        tables = camelot.read_pdf(
            pdf_path,
            pages="all",
            flavor="stream",
            password=password
        )
        return [t.df for t in tables]
    except Exception as e:
        # Some PDFs might fail table extraction, return empty list
        return []
