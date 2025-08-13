from pathlib import Path

import pdfplumber


__all__ = ("extract_text_from_pdf",)


def extract_text_from_pdf(pdf_path: Path, page_start: int, page_end: int) -> list[str]:
  """Extract text per page from a PDF between given page indexes.

  Args:
      pdf_path (Path): The path to the PDF file.
      page_start (int): The starting page number (0-indexed).
      page_end (int): The ending page number (0-indexed, exclusive).

  Returns:
      list[str]: A list of text content extracted from each page.
  """
  with pdfplumber.open(pdf_path) as pdf:
    return [page.extract_text() for page in pdf.pages[page_start:page_end]]
