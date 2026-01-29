# resume_parser.py
import os
import pdfplumber


def extract_text_from_resume(pdf_path: str) -> str:
    """
    Extracts text from a resume PDF using pdfplumber.
    Returns a single string (may be empty if PDF has no selectable text).
    """
    if not pdf_path or not os.path.exists(pdf_path):
        return f"[ERROR] File not found: {pdf_path}"

    texts = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                t = t.strip()
                if t:
                    texts.append(t)
    except Exception as e:
        return f"[ERROR] Could not read PDF: {e}"

    if not texts:
        return (
            "[WARN] No selectable text found in this PDF. "
            "It might be a scanned image PDF."
        )

    return "\n\n".join(texts)
