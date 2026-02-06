import fitz  # PyMuPDF
import os

# -------------------------------
# COMMON BAD KEYWORDS (ALL IFRS)
# -------------------------------
COMMON_BAD_KEYWORDS = [
    "CONTENTS",
    "APPENDIX",
    "ILLUSTRATIVE",
    "BASIS FOR CONCLUSIONS",
    "INTERNATIONAL FINANCIAL REPORTING STANDARD",
    "OBJECTIVE",
    "SCOPE",
    "DEFINITIONS",
]

# -------------------------------
# STANDARD-SPECIFIC BAD KEYWORDS
# -------------------------------
IFRS16_BAD = [
    "SALE AND LEASEBACK",
    "ILLUSTRATIVE EXAMPLES",
]

IFRS9_BAD = [
    "APPLICATION GUIDANCE",
    "EFFECTIVE DATE",
]

IFRS17_BAD = [
    "TRANSITION",
    "DISCLOSURE OBJECTIVES",
]

IFRS18_BAD = [
    "PRIMARY FINANCIAL STATEMENTS",
]

# -------------------------------
# FILTER FUNCTION
# -------------------------------
def is_valid_paragraph(text, standard):
    if len(text) < 150:
        return False

    for word in COMMON_BAD_KEYWORDS:
        if word.lower() in text.lower():
            return False

    standard_map = {
        "IFRS 16": IFRS16_BAD,
        "IFRS 9": IFRS9_BAD,
        "IFRS 17": IFRS17_BAD,
        "IFRS 18": IFRS18_BAD,
    }

    for word in standard_map.get(standard, []):
        if word.lower() in text.lower():
            return False

    return True

# -------------------------------
# PDF EXTRACTION FUNCTION
# -------------------------------
def extract_pdf(pdf_path, standard):
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    print(f"\n========== {standard} ==========")

    count = 1

    for page in doc:
        text = page.get_text("text")
        paragraphs = text.split("\n\n")

        for p in paragraphs:
            clean = p.strip()
            if is_valid_paragraph(clean, standard):
                print(f"{standard}-{count}: {clean[:140]}...")
                count += 1

# -------------------------------
# PDF PATHS
# -------------------------------
PDFS = {
    "IFRS 16": "media/ifrs_pdfs/ifrs16.pdf",
    "IFRS 9": "media/ifrs_pdfs/ifrs9.pdf",
    "IFRS 17": "media/ifrs_pdfs/ifrs17.pdf",
    "IFRS 18": "media/ifrs_pdfs/ifrs18.pdf",
}

# -------------------------------
# MAIN RUN
# -------------------------------
if __name__ == "__main__":
    for standard, path in PDFS.items():
        extract_pdf(path, standard)
