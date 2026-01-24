import os
import pdfplumber
import pandas as pd
from docx import Document


def load_pdf(file_path):
    documents = []

    with pdfplumber.open(file_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                documents.append({
                    "text": text.strip(),
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "type": "pdf",
                        "page": page_no
                    }
                })

    return documents


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return [{
        "text": text.strip(),
        "metadata": {
            "source": os.path.basename(file_path),
            "type": "txt"
        }
    }]


def load_docx(file_path):
    doc = Document(file_path)
    documents = []

    for para_no, para in enumerate(doc.paragraphs, start=1):
        if para.text.strip():
            documents.append({
                "text": para.text.strip(),
                "metadata": {
                    "source": os.path.basename(file_path),
                    "type": "docx",
                    "paragraph": para_no
                }
            })

    return documents


def load_excel(file_path):
    df = pd.read_excel(file_path)
    documents = []

    for row_no, row in df.iterrows():
        row_text = " | ".join(
            [f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])]
        )

        if row_text.strip():
            documents.append({
                "text": row_text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "type": "excel",
                    "row": row_no + 1
                }
            })

    return documents


def load_csv(file_path):
    df = pd.read_csv(file_path)
    documents = []

    for row_no, row in df.iterrows():
        row_text = " | ".join(
            [f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])]
        )

        if row_text.strip():
            documents.append({
                "text": row_text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "type": "csv",
                    "row": row_no + 1
                }
            })

    return documents


def load_document(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".txt":
        return load_txt(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension in [".xls", ".xlsx"]:
        return load_excel(file_path)

    elif extension == ".csv":
        return load_csv(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")
