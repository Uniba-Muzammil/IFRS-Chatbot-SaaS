import fitz  # PyMuPDF
import os

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_DIR = os.path.join(BASE_DIR, "media", "ifrs_pdfs")


# -------------------------
# LOAD ANY IFRS PDF
# -------------------------
def load_ifrs(ifrs_code):
    """
    Reads IFRS PDF and returns clean paragraph-wise data
    Works for IFRS16, IFRS9, IFRS17, IFRS18
    """

    filename = f"{ifrs_code.lower()}.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{filename} not found in media/ifrs_pdfs")

    doc = fitz.open(pdf_path)

    paragraphs = []
    para_no = 1

    for page in doc:
        text = page.get_text("text")
        raw_paras = text.split("\n\n")

        for para in raw_paras:
            para = para.strip()

            if len(para) > 50:
                paragraphs.append({
                    "ifrs": ifrs_code.upper(),
                    "para_no": para_no,
                    "text": para
                })
                para_no += 1

    return paragraphs
