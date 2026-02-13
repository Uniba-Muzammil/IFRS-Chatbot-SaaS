import re
from utils.ifrs_reader import load_ifrs


# -------------------------
# CLEAN & EXTRACT KEYWORDS
# -------------------------
def extract_keywords(question):
    """
    Extracts meaningful keywords from user question
    """
    question = question.lower()

    stopwords = {
        "what", "is", "are", "the", "how", "does", "do",
        "a", "an", "of", "to", "in", "for", "and", "on",
        "with", "be", "by", "under"
    }

    words = re.findall(r"[a-zA-Z]{3,}", question)

    keywords = [w for w in words if w not in stopwords]

    return list(set(keywords))


# -------------------------
# FIND RELEVANT PARAGRAPHS
# -------------------------
def find_relevant_paragraphs(question, ifrs_code, top_n=5):
    """
    Finds most relevant IFRS paragraphs based on keyword match
    """

    paragraphs = load_ifrs(ifrs_code)
    keywords = extract_keywords(question)

    scored_results = []

    for para in paragraphs:
        text = para["text"].lower()

        score = sum(1 for kw in keywords if kw in text)

        if score > 0:
            scored_results.append({
                "ifrs": para["ifrs"],
                "para_no": para["para_no"],
                "text": para["text"],
                "score": score
            })

    scored_results.sort(key=lambda x: x["score"], reverse=True)

    return scored_results[:top_n]

