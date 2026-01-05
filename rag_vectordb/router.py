def detect_route(question: str) -> str:
    q = question.lower()

    # KG-first intents
    kg_keywords = [
        "formula",
        "equation",
        "reaction",
        "chapter",
        "belongs to",
        "related to",
        "relationship",
        "graph",
    ]

    # Vector-first intents
    vector_keywords = [
        "explain",
        "define",
        "what is",
        "why",
        "how",
        "summary",
        "describe",
    ]

    # Web / advanced
    web_keywords = [
        "recent",
        "latest",
        "modern",
        "advancement",
        "current",
    ]

    if any(k in q for k in web_keywords):
        return "WEB"

    if any(k in q for k in kg_keywords) and any(k in q for k in vector_keywords):
        return "HYBRID"

    if any(k in q for k in kg_keywords):
        return "KG"

    return "VECTOR"
