import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def build_vector_store():
    df = pd.read_csv("data/processed/liar_clean.csv")
    real_df = df[df["binary_label"] == "real"]

    # Use the same persistent client + path that retriever.py reads from
    chroma_client = chromadb.PersistentClient(path="data/vector_db")
    collection = chroma_client.get_or_create_collection("verified_facts")

    # Use the same local embedding model retriever.py uses, so queries and
    # stored documents live in the same vector space
    model = SentenceTransformer('all-MiniLM-L6-v2')

    for idx, row in tqdm(real_df.iterrows(), total=len(real_df)):
        text = row["statement"]
        metadata = {"speaker": row["speaker"], "context": row["context"]}
        embedding = model.encode([text])[0]
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[str(idx)]
        )

    print("✅ Added embeddings to vector store (verified facts).")

if __name__ == "__main__":
    build_vector_store()
