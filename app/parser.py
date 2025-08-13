import pandas as pd

from .utils import clean_text, match_procedure


__all__ = ("parse_procedure_records",)


def parse_procedure_records(pages: list[str]) -> pd.DataFrame:
  """Parse raw page texts into structured DataFrame.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed procedure records.
  """
  records: list[dict[str, int]] = []

  for text in pages:
    for raw_line in text.split("\n"):
      line = clean_text(raw_line)

      # Procedure
      if proc_match := match_procedure(line):
        code, _, group = proc_match.groups()
        records.append(
          {"code": int(code), "group": int(group)}
        )

  return pd.DataFrame(records)
