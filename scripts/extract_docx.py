import zipfile
import xml.etree.ElementTree as ET
import sys
import io

# Force stdout to use utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_docx_text(path):
    """
    Extract text from a docx file.
    """
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }
        
        paragraphs = []
        for p in tree.findall('.//w:p', namespaces):
            texts = p.findall('.//w:t', namespaces)
            if texts:
                paragraphs.append(''.join(t.text for t in texts))
        
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_docx>")
    else:
        print(get_docx_text(sys.argv[1]))
