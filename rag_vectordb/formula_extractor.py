import re

FORMULA_PATTERN = re.compile(
    r"[A-Z][a-z]?\d*(\s*[+\-→=]\s*[A-Z][a-z]?\d*)+"
)

def extract_formulas(text):
    return list(set(FORMULA_PATTERN.findall(text)))
def extract_reactions(text):
    reactions = []
    for line in text.split("\n"):
        if "→" in line or "=" in line:
            reactions.append(line.strip())
    return reactions
