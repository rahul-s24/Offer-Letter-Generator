from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    texts = [doc.page_content for doc in chunks]

    # Correct: initialize model and wrap it using LangChain's class
    from langchain.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return FAISS.from_texts(texts, embedding=embeddings)
