import os
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_FOLDER = os.path.join(BASE_DIR, "media", "ifrspdfs")

# -------------------------
# PDF → TEXT
# -------------------------
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# -------------------------
# TEXT → CHUNKS
# -------------------------
def chunk_text(text, size=250):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


# -------------------------
# LOAD ALL IFRS 16 DATA
# -------------------------
def load_ifrs_data():
    chunks = []
    sources = []

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, file)
            text = extract_pdf_text(path)
            text_chunks = chunk_text(text)

            for chunk in text_chunks:
                chunks.append(chunk)
                sources.append(file)

    return chunks, sources


# -------------------------
# ANSWER USER QUESTION
# -------------------------
def find_relevant_paragraph(question):
    chunks, sources = load_ifrs_data()

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(chunks + [question])

    scores = cosine_similarity(vectors[-1], vectors[:-1])
    best_index = scores.argmax()

    return {
        "pdf": sources[best_index],
        "text": chunks[best_index]
    }
