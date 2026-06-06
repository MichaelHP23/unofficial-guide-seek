import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("seek_guide")

def retrieve(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 3)
        })
    return chunks

if __name__ == "__main__":
    test_queries = [
        "How do I apply to SEEK?",
        "What financial support does SEEK provide?",
        "What do students say about SEEK advisors?"
    ]
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("─" * 50)
        results = retrieve(query)
        for r in results:
            print(f"Source: {r['source']} | Distance: {r['distance']}")
            print(r['text'][:150])
            print()