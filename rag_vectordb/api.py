from flask import Flask, request, jsonify
from service import RAGService

app = Flask(__name__)

rag = RAGService()
rag.load()

@app.post("/ask")
def ask():
    data = request.json or {}

    query = data.get("query")
    allow_web = data.get("allow_web", False)

    # Debug logging
    print(f"API DEBUG: query='{query}', allow_web={allow_web}")

    answer, route = rag.answer(query, allow_web=allow_web, return_route=True)

    print(f"API DEBUG: route='{route}', answer_preview='{answer[:100]}...'")

    return {
        "answer": answer,
        "route": route
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=8000, debug=True)
