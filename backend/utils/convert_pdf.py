import pdfplumber
import re

JUNK_KEYWORDS = [
    "© IFRS Foundation",
    "Basis for Conclusions",
    "Illustrative Examples",
    "Approval by the Board",
    "FOR THE ACCOMPANYING GUIDANCE",
    "Part B of this edition",
    "Part C of this edition"
]

def is_heading(line):
    line = line.strip()

    if len(line) < 5:
        return False

    if len(line) < 70 and line.isupper():
        return True

    return False


def clean_line(line):
    line = line.strip()

    # Remove page numbers
    if re.fullmatch(r"[A]?\d+", line):
        return ""

    for junk in JUNK_KEYWORDS:
        if junk.lower() in line.lower():
            return ""

    return line


def extract_clean_paragraphs(pdf_path, standard_name):
    paragraphs = []
    current_section = "General"
    para_counter = 1
    buffer = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for raw_line in lines:

                line = clean_line(raw_line)

                if not line:
                    continue

                if is_heading(line):
                    current_section = line
                    continue

                if len(line) > 40:
                    buffer += " " + line

                if buffer.strip().endswith("."):
                    paragraphs.append({
                        "standard": standard_name,
                        "section": current_section,
                        "para_id": f"{standard_name}_{para_counter}",
                        "text": buffer.strip()
                    })
                    para_counter += 1
                    buffer = ""

    return paragraphs
