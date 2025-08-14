import pandas as pd

from .utils import (
  clean_text,
  match_procedure,
  match_surgical_fee,
  search_professional_services,
)


__all__ = ("parse_procedure_records", "parse_surgical_professional_fees")


def parse_procedure_records(pages: list[str]) -> pd.DataFrame:
  """Parse raw page texts into structured DataFrame.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed procedure records
        with "code" and "group" columns.
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

def parse_surgical_professional_fees(pages: list[str]) -> pd.DataFrame:
  """Parse surgical professional fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed surgical professional fees
        with "code", "group", and "Fee (S.M.L.D.V)" columns.
  """
  records: list[dict[str, int | float | bool]] = []

  page = pages[0]
  match = search_professional_services(page)
  result = page[match.start():].split("\n") if match else []
  rows = result[1:-1]

  def get_record(row: str) -> dict[str, int | float | bool]:
    """Extracts a record from a row of text."""
    row_match = match_surgical_fee(row)
    if not row_match:
      return {}
    return {
      "code": int(row_match.group(1)),
      "group": int(row_match.group(2).split()[-1]),
      "special": str(row_match.group(2)).find("especial") != -1,
      "Fee (S.M.L.D.V)": float(row_match.group(3).replace(",", ".")),
      "Fee (COP)": int(row_match.group(4).replace(".", "")),
    }

  records = [get_record(row) for row in rows if get_record(row)]
  return pd.DataFrame(records)
