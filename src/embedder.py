import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import chromadb
from tqdm import tqdm

# Load .env file
load_dotenv()

# Initialize client with key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_vector_store():
    df = pd.read_csv("data/processed/liar_clean.csv")
    real_df = df[df["binary_label"] == "real"]

    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection("verified_facts")

    for idx, row in tqdm(real_df.iterrows(), total=len(real_df)):
        text = row["statement"]
        metadata = {"speaker": row["speaker"], "context": row["context"]}
        collection.add(documents=[text], metadatas=[metadata], ids=[str(idx)])

    print("✅ Added embeddings to vector store (verified facts).")

if __name__ == "__main__":
    build_vector_store()
