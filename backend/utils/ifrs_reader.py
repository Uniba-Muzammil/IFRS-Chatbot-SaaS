import fitz
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_DIR = os.path.join(BASE_DIR, "media", "ifrs_pdfs")


def load_ifrs_paragraphs(ifrs_code):

    filename = f"{ifrs_code.lower()}.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{filename} not found.")

    doc = fitz.open(pdf_path)

    paragraphs = []

    for page in doc:
        text = page.get_text("text")
        raw_paras = text.split("\n\n")

        for para in raw_paras:
            para = para.strip()

            if len(para) > 80:
                match = re.match(r"^([A-Z]?\d+[A-Z]?)", para)
                para_no = match.group(1) if match else None

                paragraphs.append({
                    "ifrs": ifrs_code.upper(),
                    "para_no": para_no,
                    "text": para
                })

    return paragraphs
