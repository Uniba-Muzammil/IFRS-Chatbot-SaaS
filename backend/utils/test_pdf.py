import fitz
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "media", "ifrs_pdfs")

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        print("\n==============================")
        print(f"📘 Reading {file}")
        print("==============================\n")

        pdf_path = os.path.join(PDF_DIR, file)
        doc = fitz.open(pdf_path)

        for page_no, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if text:
                print(f"\n--- Page {page_no} ---\n")
                print(text[:1000])  # sirf first 1000 chars (terminal safe)

