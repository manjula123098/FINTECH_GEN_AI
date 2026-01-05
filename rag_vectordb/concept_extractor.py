import re

def extract_concepts(text):
    concepts = []

    for line in text.split("\n"):
        line = line.strip()

        if len(line) < 5:
            continue

        # Simple heuristic
        if line.isupper() and len(line.split()) <= 6:
            concepts.append(line.title())

        if line.lower().startswith("definition"):
            parts = line.split(":")
            if len(parts) > 1:
                concepts.append(parts[1].strip().title())

    return list(set(concepts))
