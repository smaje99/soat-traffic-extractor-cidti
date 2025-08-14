import pandas as pd

from .utils import (
  clean_text,
  match_procedure,
  match_surgical_fee,
  search_professional_services,
)


__all__ = ("parse_procedure_records", "parse_surgeon_fees", "parse_anesthesiologist_fees")


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
        records.append({"code": int(code), "group": int(group)})

  return pd.DataFrame(records)


def parse_fee_records(fees: list[str]) -> pd.DataFrame:
  """Parse raw fee records into structured DataFrame.

  Args:
      fees (list[str]): A list of raw fee records.

  Returns:
      pd.DataFrame: A DataFrame containing parsed fee records
        with "code", "group", "special", "Fee (S.M.L.D.V) and Fee (COP)" columns.
  """
  records: list[dict[str, int | float | bool]] = []

  for fee in fees:
    if fee_match := match_surgical_fee(fee):
      code, group, fee_sml, fee_cop = fee_match.groups()
      records.append(
        {
          "code": int(code),
          "group": int(group.split()[-1]),
          "special": group.find("especial") != -1,
          "Fee (S.M.L.D.V)": float(fee_sml.replace(",", ".")),
          "Fee (COP)": int(fee_cop.replace(".", "")),
        }
      )

  return pd.DataFrame(records)


def parse_surgeon_fees(pages: list[str]) -> pd.DataFrame:
  """Parse surgical professional fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed surgical professional fees
        with "code", "group", "special", "Fee (S.M.L.D.V) and Fee (COP)" columns.
  """
  page = pages[0]
  match = search_professional_services(page)
  result = page[match.start() :].split("\n") if match else []
  rows = result[1:-1]

  return parse_fee_records(rows)


def parse_anesthesiologist_fees(pages: list[str]) -> pd.DataFrame:
  """Parse anesthesiologist fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed anesthesiologist fees
        with "code", "group", "special", "Fee (S.M.L.D.V) and Fee (COP)" columns.
  """
  lines = pages[0].split("\n")
  rows = lines[2:18]

  return parse_fee_records(rows)
