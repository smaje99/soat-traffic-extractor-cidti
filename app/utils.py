import re
from re import Match


__all__ = ("clean_text", "match_procedure")


def clean_text(text: str) -> str:
  """Normalize spaces and strip leading/trailing whitespace.

  Args:
      text (str): The text to clean.

  Returns:
      str: The cleaned text.
  """
  return re.sub(r"\s+", " ", text).strip()


def match_procedure(line: str) -> Match[str] | None:
  """Match procedure table rows: code + description + group.

  Args:
      line (str): The input line to match.

  Returns:
      Match[str] | None: The match object if successful, None otherwise.
  """
  return re.match(r"^(\d{4,5})\s+(.*?)\s+(\d+)$", line.strip())
