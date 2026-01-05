from kg_store import KGStore

kg = None

def get_kg():
    global kg
    if kg is None:
        try:
            kg = KGStore()
        except Exception:
            return None
    return kg

def query_kg(question: str):
    kg = get_kg()
    if kg is None:
        return None
    
    q = question.lower()

    if "formula" in q and "rust" in q:
        r = kg.run("""
        MATCH (c:Concept {name:"Rusting of Iron"})-[:HAS_FORMULA]->(f)
        RETURN f.expression AS formula
        """)
        return r[0]["formula"] if r else None

    if "chapter" in q and "rust" in q:
        r = kg.run("""
        MATCH (c:Concept {name:"Rusting of Iron"})-[:BELONGS_TO]->(ch)
        RETURN ch.name AS chapter
        """)
        return r[0]["chapter"] if r else None

    return None
