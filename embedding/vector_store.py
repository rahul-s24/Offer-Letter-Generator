from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.docstore.document import Document

def create_vector_store(chunks):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    documents = [Document(page_content=c) for c in chunks]
    db = FAISS.from_documents(documents, embedding_model)
    return db
