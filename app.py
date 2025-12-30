from flask import Flask, request, jsonify
from flask_cors import CORS
from src.rag_pipeline import FakeNewsRAG

app = Flask(__name__)
CORS(app)

rag = FakeNewsRAG()

@app.route("/api/check", methods=["POST"])
def check_claim():
    data = request.get_json()
    claim = data.get("claim", "")
    result = rag.check_claim(claim)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
