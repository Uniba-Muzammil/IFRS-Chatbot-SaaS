import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from ifrs_reader import load_ifrs_paragraphs


# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Index storage directory
INDEX_DIR = os.path.join(BASE_DIR, "indexes")

# Create indexes folder if it does not exist
os.makedirs(INDEX_DIR, exist_ok=True)


def build_index(ifrs_code):
    print(f"Building index for {ifrs_code}...")

    # Load paragraphs from your IFRS reader
    paragraphs = load_ifrs_paragraphs(ifrs_code)

    if not paragraphs:
        print(f"No paragraphs found for {ifrs_code}")
        return

    documents = []

    for para in paragraphs:
        documents.append(
            Document(
                page_content=para["text"],
                metadata={
                    "ifrs": para["ifrs"],
                    "para_no": para["para_no"]
                }
            )
        )

    # Load embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store
    vector_store = FAISS.from_documents(documents, embeddings)

    # Save index locally
    save_path = os.path.join(INDEX_DIR, ifrs_code.lower())
    vector_store.save_local(save_path)

    print(f"✅ {ifrs_code} index built successfully at {save_path}\n")


if __name__ == "__main__":
    try:
        build_index("IFRS16")
        build_index("IFRS17")
        build_index("IFRS18")
        build_index("IFRS9")
        print("🎉 All indexes built successfully.")
    except Exception as e:
        print("❌ Error occurred:")
        print(e)

