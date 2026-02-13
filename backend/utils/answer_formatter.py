# utils/answer_formatter.py

def format_ifrs_answer(question, matched_paragraphs):
    """
    matched_paragraphs = list of dicts
    each dict:
    {
        ifrs,
        para_no,
        text,
        score
    }
    """

    top_para = matched_paragraphs[0]

    response = {
        "answer": generate_simple_answer(top_para["text"]),
        "reference": f'{top_para["ifrs"]} Para {top_para["para_no"]}',
        "official_text": top_para["text"],
        "auditor_focus": infer_auditor_focus(top_para["text"]),
        "disclaimer": "For educational use only"
    }

    return response


def generate_simple_answer(text):
    sentences = text.replace("\n", " ").split(".")
    for s in sentences:
        s = s.strip()
        if len(s) > 40 and "shall" in s.lower():
            return s + "."
    return sentences[0][:200] + "..."




def infer_auditor_focus(text):
    t = text.lower()

    if "discount rate" in t or "borrowing rate" in t or "present value" in t:
        return "Discount rate judgment"
    if "lease term" in t:
        return "Lease term estimation"
    if "option" in t:
        return "Management option assessment"

    return "Management judgment involved"
