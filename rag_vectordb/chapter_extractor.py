import re

# More precise patterns to detect actual chapter headings
CHAPTER_PATTERNS = [
    re.compile(r"^CHAPTER\s+(\d+)\s*[:\-]?\s*(.+)$", re.IGNORECASE),
    re.compile(r"^Chapter\s+(\d+)\s*[:\-]?\s*(.+)$", re.IGNORECASE),
    re.compile(r"^UNIT\s+(\d+)\s*[:\-]?\s*(.+)$", re.IGNORECASE),
    re.compile(r"^Unit\s+(\d+)\s*[:\-]?\s*(.+)$", re.IGNORECASE),
    # More specific pattern for numbered sections that are likely real chapters
    re.compile(r"^(\d+)\.\s+([A-Z][A-Za-z\s,.-]{15,})$"),  # "1. Chemical Reactions and Equations"
]

def detect_chapters(pages):
    chapters = []
    seen_chapters = set()  # To avoid duplicates
    
    for p in pages:
        lines = p["text"].split("\n")
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 10:
                continue
                
            # Try each pattern
            for pattern in CHAPTER_PATTERNS:
                match = pattern.match(line)
                if match:
                    chapter_num = match.group(1)
                    chapter_name = match.group(2).strip()
                    
                    # Filter out very short names, common false positives, and duplicates
                    if (len(chapter_name) > 15 and 
                        not any(word in chapter_name.lower() for word in 
                               ['page', 'figure', 'table', 'exercise', 'example', 'answer', 'question', 
                                'what', 'how', 'why', 'explain', 'write', 'draw', 'solve']) and
                        chapter_name not in seen_chapters):
                        
                        chapters.append({
                            "number": chapter_num,
                            "name": chapter_name,
                            "page": p["page"],
                            "line": line_num
                        })
                        seen_chapters.add(chapter_name)
                        break  # Found a match, no need to try other patterns
    
    # Sort by chapter number
    try:
        chapters.sort(key=lambda x: int(x["number"]))
    except:
        pass  # Keep original order if sorting fails
        
    return chapters

def detect_chapters_from_file(pdf_path="data/10th_science.pdf"):
    """Convenience function with correct default filename"""
    from pdf_reader import extract_pages
    pages = extract_pages(pdf_path)
    return detect_chapters(pages)
