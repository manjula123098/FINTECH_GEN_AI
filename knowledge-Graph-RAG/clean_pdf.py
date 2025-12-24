#!/usr/bin/env python
import pdfplumber
from pathlib import Path

pdf_path = Path('sample_data/NEP_Final_English_0.pdf')
text = ''

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + '\n'

# Clean up encoding issues
text = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

# Remove excessive whitespace
text = '\n'.join(line.rstrip() for line in text.split('\n'))

output_path = Path('sample_data/api_documentation.txt')
output_path.write_text(text, encoding='utf-8')
print(f'Extracted and cleaned {len(text)} characters from PDF')
print(f'Saved to {output_path}')
