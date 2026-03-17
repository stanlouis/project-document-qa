# core/chunker.py
import tiktoken
import fitz  # PyMuPDF
from typing import List

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts raw text from a PDF document."""
    text = ""
    try:
        # Open the PDF file
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text() + "\n"
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")
        
    return text

def chunk_text(text: str, max_tokens: int = 500, overlap: int = 100, model: str = "gpt-4o-mini") -> List[str]:
    """Splits text into overlapping chunks based on token count."""
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk = enc.decode(tokens[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap

    return chunks