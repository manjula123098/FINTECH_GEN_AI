from kg_store import KGStore

kg = KGStore()

# Chapter
kg.run("""
MERGE (c:Chapter {name:$name})
""", {"name": "Metals and Non-metals"})

# Concept
kg.run("""
MATCH (c:Chapter {name:$chapter})
MERGE (x:Concept {name:$concept})
MERGE (x)-[:BELONGS_TO]->(c)
""", {
    "chapter": "Metals and Non-metals",
    "concept": "Rusting of Iron"
})

# Formula
kg.run("""
MATCH (x:Concept {name:$concept})
MERGE (f:Formula {expression:$formula})
MERGE (x)-[:HAS_FORMULA]->(f)
""", {
    "concept": "Rusting of Iron",
    "formula": "Fe → Fe²⁺ + 2e⁻"
})

print("✅ KG ingestion completed")
