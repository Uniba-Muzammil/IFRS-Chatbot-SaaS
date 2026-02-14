import os
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(BASE_DIR, "indexes")


def search_ifrs(ifrs_code, question, k=1):
    """
    Search the FAISS index for a given IFRS standard and question.

    Args:
        ifrs_code (str): IFRS standard code, e.g., "ifrs9"
        question (str): The query text
        k (int): Number of top matches to return

    Returns:
        dict: {'text', 'ifrs', 'para_no'} or None if no match found
    """

    # Folder for this standard
    index_path = os.path.join(INDEX_DIR, ifrs_code.lower())

    # Check if index exists
    faiss_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(faiss_file):
        print(f"[ERROR] FAISS index not found at {index_path}")
        return None

    try:
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load FAISS vector store along with metadata (.pkl)
        vector_store = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        # Run similarity search
        results = vector_store.similarity_search(question, k=k)
        if not results:
            return None

        doc = results[0]  # top result
        return {
            "text": doc.page_content,
            "ifrs": doc.metadata.get("ifrs", ifrs_code),
            "para_no": doc.metadata.get("para_no", "?")
        }

    except Exception as e:
        print(f"[ERROR] Failed to search FAISS for {ifrs_code}: {e}")
        return None
