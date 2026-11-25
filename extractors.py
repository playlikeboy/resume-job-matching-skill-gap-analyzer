from __future__ import annotations

from io import BytesIO
from pathlib import Path


def extract_resume_text(filename: str, content: bytes) -> str:
    """Extract selectable text from PDF or DOCX; scanned-PDF OCR is out of scope."""
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        try:
            import fitz  # PyMuPDF
        except ImportError as exc:  # pragma: no cover - dependency error guidance
            raise ValueError("PDF support is unavailable. Install backend requirements.") from exc
        try:
            with fitz.open(stream=content, filetype="pdf") as document:
                return "\n".join(page.get_text("text") for page in document).strip()
        except Exception as exc:
            raise ValueError("The PDF could not be read. Check that it is a valid, non-password-protected PDF.") from exc

    if suffix == ".docx":
        try:
            from docx import Document
            document = Document(BytesIO(content))
            paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
            table_text = [cell.text for table in document.tables for row in table.rows for cell in row.cells]
            return "\n".join(paragraphs + table_text).strip()
        except Exception as exc:
            raise ValueError("The DOCX could not be read. Check that it is a valid Word document.") from exc

    raise ValueError("Unsupported file type. Upload a PDF or DOCX file.")
