# backend/utils/paragraph_matcher.py

import re
from collections import Counter

# -----------------------------
# STEP 1: clean & tokenize text
# -----------------------------
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.split()

# -----------------------------
# STEP 2: keyword extraction
# -----------------------------
def extract_keywords(question):
    stopwords = {
        "what", "is", "the", "how", "are", "of", "in",
        "to", "for", "and", "a", "an", "does", "be"
    }
    words = tokenize(question)
    return [w for w in words if w not in stopwords]

# -----------------------------
# STEP 3: paragraph scoring
# -----------------------------
def score_paragraph(paragraph_text, keywords):
    paragraph_words = tokenize(paragraph_text)
    word_counts = Counter(paragraph_words)

    score = 0
    for kw in keywords:
        score += word_counts.get(kw, 0)

    return score

# -----------------------------
# STEP 4: match best paragraphs
# -----------------------------
def find_relevant_paragraphs(question, paragraphs, top_n=3):
    """
    paragraphs = list of dicts
    [
      {
        "ifrs": "IFRS16",
        "para_no": "26",
        "text": "At the commencement date..."
      }
    ]
    """

    keywords = extract_keywords(question)

    scored = []
    for para in paragraphs:
        score = score_paragraph(para["text"], keywords)
        if score > 0:
            scored.append((score, para))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [para for score, para in scored[:top_n]]
