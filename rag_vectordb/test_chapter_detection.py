from pdf_reader import extract_pages
from chapter_extractor import detect_chapters

# Test with automatic filename correction
print("Testing chapter detection...")
try:
    # This will automatically use 10th_science.pdf even if you type science.pdf
    pages = extract_pages("data/science.pdf")  # Will be auto-corrected
    chapters = detect_chapters(pages)
    
    print(f"Found {len(chapters)} chapters:")
    for chapter in chapters:
        print(f"  Chapter {chapter['number']}: {chapter['name']} (Page {chapter['page']})")
        
    if not chapters:
        print("No chapters detected. Showing first few pages content for debugging:")
        for i in range(min(3, len(pages))):
            print(f"\nPage {pages[i]['page']} (first 200 chars):")
            print(pages[i]['text'][:200] + "...")
            
except Exception as e:
    print(f"Error: {e}")