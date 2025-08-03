from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def load_and_chunk_policies(paths):
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    for path in paths:
        reader = PdfReader(path)
        raw_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        doc_chunks = splitter.split_text(raw_text)
        chunks.extend(doc_chunks)

    return chunks
