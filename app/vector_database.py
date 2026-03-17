import chromadb

# Persistent client — app restart pe data rehta hai
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="website_data")


def store_chunks(chunks: list[str], url: str = ""):
    """Chunks ko ChromaDB mein store karo. IDs unique rakhne ke liye url+index use karo."""
    existing_count = collection.count()
    ids = [f"{url}_{existing_count + i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids,
    )


def search_chunks(query: str, k: int = 5) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=k,
    )
    return results["documents"][0]
