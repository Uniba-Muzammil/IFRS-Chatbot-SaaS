import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from utils.convert_pdf import extract_clean_paragraphs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_FOLDER = os.path.join(BASE_DIR, "media", "ifrs_pdfs")
INDEX_FOLDER = os.path.join(BASE_DIR, "indexes")

STANDARDS = {
    "ifrs9": "ifrs9.pdf",
    "ifrs16": "ifrs16.pdf",
    "ifrs17": "ifrs17.pdf",
    "ifrs18": "ifrs18.pdf"
}

def build_index(standard_key, pdf_file):

    pdf_path = os.path.join(PDF_FOLDER, pdf_file)

    print(f"Processing {standard_key}...")

    data = extract_clean_paragraphs(pdf_path, standard_key.upper())

    documents = []

    for item in data:
        documents.append(
            Document(
                page_content=item["text"],
                metadata={
                    "standard": item["standard"],
                    "section": item["section"],
                    "para_id": item["para_id"]
                }
            )
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)

    save_path = os.path.join(INDEX_FOLDER, standard_key)

    vectorstore.save_local(save_path)

    print(f"{standard_key} index built successfully!")


if __name__ == "__main__":

    for key, pdf_file in STANDARDS.items():
        build_index(key, pdf_file)

    print("All indexes built successfully!")
