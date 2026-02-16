from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def search_ifrs(standard, question):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        f"indexes/{standard.lower()}",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=1)

    result = docs[0]

    return {
        "text": result.page_content,
        "standard": result.metadata["standard"],
        "section": result.metadata["section"],
        "para_id": result.metadata["para_id"]
    }
