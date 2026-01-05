from pdf_reader import extract_pages

pages = extract_pages('data/10th_science.pdf')
print('First page content (first 1000 chars):')
print(repr(pages[0]['text'][:1000]))
print()
print('Looking for chapter-like patterns in first 10 pages:')
for i in range(min(10, len(pages))):
    lines = pages[i]['text'].split('\n')
    for line in lines:
        if any(word in line.lower() for word in ['chapter', 'unit', 'lesson']):
            print(f'Page {pages[i]["page"]}: {line.strip()}')