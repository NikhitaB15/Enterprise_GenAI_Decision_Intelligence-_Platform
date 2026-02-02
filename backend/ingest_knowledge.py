import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, '..', 'docs')
DB_DIR = os.path.join(BASE_DIR, '..', 'data', 'vector_db')

def ingest_docs():
    print("Loading documents...")
    docs = []
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".md"):
            path = os.path.join(DOCS_DIR, filename)
            loader = TextLoader(path)
            docs.extend(loader.load())
    
    print(f"Loaded {len(docs)} documents.")

    # Split
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f"Split into {len(splits)} chunks.")

    # Embed and Store
    print("Embedding and storing in ChromaDB (locally via HuggingFace)...")
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_DIR
    )
    
    # Simple check
    count = vectorstore._collection.count()
    print(f"Success! Vector DB now contains {count} chunks.")

if __name__ == "__main__":
    ingest_docs()
