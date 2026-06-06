from sentence_transformers import SentenceTransformer
import chromadb
from ingest import run_ingestion

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Delete collection if it exists so we start fresh
try:
    client.delete_collection("seek_guide")
except:
    pass

collection = client.create_collection("seek_guide")

def embed_and_store(chunks):
    print(f"Embedding {len(chunks)} chunks...")
    
    texts = [c["text"] for c in chunks]
    ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"], "type": c["type"]} for c in chunks]
    
    embeddings = model.encode(texts, show_progress_bar=True)
    
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB")

if __name__ == "__main__":
    chunks = run_ingestion()
    embed_and_store(chunks)
    print("Done. Vector store ready.")