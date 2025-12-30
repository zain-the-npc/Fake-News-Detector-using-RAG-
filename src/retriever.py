import chromadb
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, collection_name="verified_facts"):
        # Use persistent client so your vector database is saved on disk
        self.chroma_client = chromadb.PersistentClient(path="data/vector_db")

        # Create or load an existing Chroma collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )

        # Load a local embedding model (runs offline)
        # You can use CPU or GPU by adding device='cuda' if you have one
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def query(self, text, top_k=5):
        """
        Takes an input text (claim), encodes it using a local embedding model,
        then performs semantic search on the ChromaDB collection.
        Returns the top_k most relevant fact documents.
        """
        # Create the embedding locally — no API call, no cost, very fast
        query_embedding = self.model.encode([text])[0]

        # Query the Chroma vector store
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # Return the list of matched documents
        return results["documents"][0]
