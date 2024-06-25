from docx import Document

def read_docx_text(file_path):
    """Reads text from a .docx file and stores it in a variable.
    """

    doc = Document(file_path)
    all_paragraphs = ""

    for paragraph in doc.paragraphs:
        all_paragraphs += paragraph.text + "\n"
        
    return all_paragraphs