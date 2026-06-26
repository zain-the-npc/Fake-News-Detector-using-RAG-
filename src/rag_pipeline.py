import os
from dotenv import load_dotenv
from openai import OpenAI
from src.retriever import Retriever

# Load the environment variables
load_dotenv()

# Initialize the OpenAI client securely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FakeNewsRAG:
    def __init__(self):
        self.retriever = Retriever()

    # rag_pipeline.py (replace check_claim with this version)
    def check_claim(self, claim):
        facts = self.retriever.query(claim, top_k=5)
        context = "\n".join([f"- {f}" for f in facts])

        prompt = f"""
        You are a fact-checking assistant.

        Claim: "{claim}"

        Verified facts:
        {context}

        Based on these facts, classify the claim as True, False, or Unverified.
        Give a short reasoning.
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI fact-checking assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        response = completion.choices[0].message.content
        response_lower = response.lower()
        verdict = "Unverified"
        # Check negated forms first so "not true" / "isn't false" don't get misread
        if "not true" in response_lower or "false" in response_lower:
            verdict = "False"
        elif "true" in response_lower:
            verdict = "True"

        return {
            "verdict": verdict,
            "reasoning": response,
            "facts": facts  # <-- added this line
        }
