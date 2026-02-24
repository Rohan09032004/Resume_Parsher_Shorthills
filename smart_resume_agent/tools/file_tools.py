from pathlib import Path
from typing import Optional

import pdfplumber


def extract_pdf_text(filepath: str) -> str:
    """
    Extract raw text from a PDF resume file.

    Args:
        filepath: Absolute or relative path to a PDF file.

    Returns:
        The extracted text content as a single string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not .pdf or no text is found.
    """
    path = Path(filepath).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported by extract_pdf_text.")

    texts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text: Optional[str] = page.extract_text()
            if page_text:
                texts.append(page_text)

    combined = "\n".join(texts).strip()
    if not combined:
        raise ValueError("No text could be extracted from the PDF.")

    return combined

