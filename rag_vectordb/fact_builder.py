def build_facts(chapter, page_text):
    return {
        "chapter": chapter,
        "concepts": extract_concepts(page_text),
        "formulas": extract_formulas(page_text),
        "reactions": extract_reactions(page_text),
    }
def validate_fact(fact):
    if not fact["concepts"] and not fact["formulas"]:
        return False
    return True
