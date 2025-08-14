import re
from re import Match


__all__ = (
  "clean_text",
  "match_procedure",
  "search_professional_services",
  "match_surgical_fee",
)


def clean_text(text: str) -> str:
  """Normalize spaces and strip leading/trailing whitespace."""
  return re.sub(r"\s+", " ", text).strip()


def match_procedure(line: str) -> Match[str] | None:
  """Match procedure table rows: code + description + group."""
  return re.match(r"^(\d{4,5})\s+(.*?)\s+(\d+)$", line.strip())


def search_professional_services(text: str) -> Match[str] | None:
  """Search for professional services in the text."""
  return re.search(r"1.\sServicios profesionales del cirujano o ginecoobstetra:", text)


def match_surgical_fee(line: str) -> Match[str] | None:
  """Match surgical fee table rows: code + group + fee (S.M.L.D.V) + fee (COP)."""
  return re.match(
    r"^(\d{5})\s+(Grupo\s+(?:\d+|especial\s+\d+))\s+([\d,]+)\s+([\d\.]+)$",
    line,
    re.IGNORECASE,
  )
