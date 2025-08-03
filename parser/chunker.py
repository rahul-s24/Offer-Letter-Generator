from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk(filepath, chunk_size=1000, chunk_overlap=100):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.create_documents([text])
    return chunks
