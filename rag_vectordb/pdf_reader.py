import pdfplumber
import os
import warnings
import sys
from io import StringIO

def get_correct_pdf_path(pdf_path):
    """Map common incorrect filenames to the correct one"""
    if pdf_path == "data/science.pdf":
        return "data/10th_science.pdf"
    return pdf_path

def extract_pages(pdf_path):
    # Automatically correct the filename if needed
    pdf_path = get_correct_pdf_path(pdf_path)
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}. Available files: {os.listdir('data') if os.path.exists('data') else 'data directory not found'}")
    
    pages = []
    
    # More aggressive warning suppression
    warnings.filterwarnings("ignore")
    
    # Capture stderr to suppress the specific error messages
    old_stderr = sys.stderr
    sys.stderr = StringIO()
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text()
                    if text:
                        pages.append({
                            "page": i,
                            "text": text.strip()
                        })
                except Exception as e:
                    # Skip pages that can't be processed
                    continue
    except Exception as e:
        # Restore stderr to show this error
        sys.stderr = old_stderr
        print(f"Error processing PDF {pdf_path}: {e}")
        return []
    finally:
        # Always restore stderr
        sys.stderr = old_stderr
    
    return pages
