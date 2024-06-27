from docx import Document


# Reads text from a .docx file and stores it in a variable.
def read_docx_text(file_path):
    doc = Document(file_path)
    all_paragraphs = ""

    for paragraph in doc.paragraphs:
        all_paragraphs += paragraph.text + "\n"
        
    return all_paragraphs