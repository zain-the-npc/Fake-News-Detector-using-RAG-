from rag_pipeline import FakeNewsRAG

if __name__ == "__main__":
    print("📰 Fake News Detection System (RAG + ChatGPT API)")
    print("------------------------------------------------")
    rag = FakeNewsRAG()

    while True:
        claim = input("\nEnter a news claim (or type 'exit'): ").strip()
        if claim.lower() == "exit":
            print("👋 Exiting. Goodbye!")
            break

        result = rag.check_claim(claim)
        print("\n🧠 Verdict:", result["verdict"])
        print("💬 Reasoning:\n", result["reasoning"])
