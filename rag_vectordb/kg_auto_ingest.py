from kg_store import KGStore
from pdf_reader import extract_pages
from chapter_extractor import detect_chapters
from concept_extractor import extract_concepts
from formula_extractor import extract_formulas, extract_reactions

print("🚀 Starting Knowledge Graph Auto-Ingestion...")

try:
    kg = KGStore()
    print("✅ Connected to Knowledge Graph database")
except Exception as e:
    print(f"❌ Failed to connect to Knowledge Graph: {e}")
    exit(1)

try:
    print("📖 Extracting pages from PDF...")
    pages = extract_pages("data/10th_science.pdf")
    print(f"✅ Extracted {len(pages)} pages")
except Exception as e:
    print(f"❌ Failed to extract pages: {e}")
    exit(1)

try:
    print("📑 Detecting chapters...")
    chapters = detect_chapters(pages)
    print(f"✅ Found {len(chapters)} chapters")
except Exception as e:
    print(f"❌ Failed to detect chapters: {e}")
    chapters = []

print("💾 Ingesting data into Knowledge Graph...")

for ch in chapters:
    try:
        kg.run("""
        MERGE (c:Chapter {number:$num, name:$name})
        """, {"num": ch["number"], "name": ch["name"]})
        print(f"  📚 Chapter {ch['number']}: {ch['name']}")
    except Exception as e:
        print(f"  ❌ Error adding chapter {ch.get('number', '?')}: {e}")
        continue

    for p in pages:
        if p["page"] >= ch["page"]:
            try:
                concepts = extract_concepts(p["text"])
                formulas = extract_formulas(p["text"])

                for con in concepts:
                    kg.run("""
                    MATCH (c:Chapter {name:$chapter})
                    MERGE (x:Concept {name:$concept})
                    MERGE (x)-[:BELONGS_TO]->(c)
                    """, {"chapter": ch["name"], "concept": con})

                for f in formulas:
                    kg.run("""
                    MATCH (c:Concept)
                    MERGE (f:Formula {expression:$expr})
                    """, {"expr": f})
            except Exception as e:
                print(f"  ⚠️  Error processing page {p['page']}: {e}")
                continue

print("✅ Knowledge Graph ingestion completed!")
