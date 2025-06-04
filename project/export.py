from pathlib import Path
from docx import Document


def export_txt(text: str, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def export_docx(text: str, path: str):
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(path)
