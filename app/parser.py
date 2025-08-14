import pandas as pd

from .utils import (
  clean_text,
  match_pre_consultation_fee,
  match_procedure,
  match_surgical_assistant_services,
  match_surgical_fee,
  pattern_material_fee,
  search_professional_services,
)


__all__ = (
  "parse_anesthesiologist_fees",
  "parse_material_fees",
  "parse_operating_room_fees",
  "parse_pre_consultation_fees",
  "parse_procedure_records",
  "parse_surgeon_fees",
  "parse_surgical_assistant_fees",
)


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


def parse_surgical_assistant_fees(pages: list[str]) -> pd.DataFrame:
  """Parse surgical assistant fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed surgical assistant fees
        with "code", "group", "special", "Fee (S.M.L.D.V) and Fee (COP)" columns.
  """
  page = pages[0]
  match = match_surgical_assistant_services(page)
  lines = page[match.start() :].split("\n") if match else []
  rows = lines[1:13]

  return parse_fee_records(rows)


def parse_pre_consultation_fees(pages: list[str]) -> pd.DataFrame:
  """Parse pre-consultation fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed pre-consultation fees
        with "code", "description", "Fee (S.M.L.D.V)" and "Fee (COP)" columns.
  """
  records: list[dict[str, int | str | float]] = []
  page = pages[0]
  index = page.index("39137")
  lines = page[index:].split("\n") if index != -1 else []
  rows = [lines[0], lines[2]]

  for row in rows:
    if match := match_pre_consultation_fee(row):
      code, description, fee_sml, fee_cop = match.groups()
      records.append(
        {
          "code": int(code),
          "description": description,
          "Fee (S.M.L.D.V)": float(fee_sml.replace(",", ".")),
          "Fee (COP)": int(fee_cop.replace(".", "")),
        }
      )

  return pd.DataFrame(records)


def parse_operating_room_fees(pages: list[str]) -> pd.DataFrame:
  """Parse operating room fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed operating room fees
        with "code", "group", "special", "Fee (S.M.L.D.V) and Fee (COP)" columns.
  """
  page = pages[0]
  index = page.index("39204")
  result = page[index:].split("\n") if index != -1 else []
  rows = result[0:16]

  return parse_fee_records(rows)


def parse_material_fees(pages: list[str]) -> pd.DataFrame:
  """Parse material fees from raw page texts.

  Args:
      pages (list[str]): A list of raw page texts.

  Returns:
      pd.DataFrame: A DataFrame containing parsed material fees
        with "code", "group", "raw_group", "Fee (S.M.L.D.V)" and "Fee (COP)" columns.
  """
  records: list[dict[str, int | str | float]] = []
  page = pages[0]
  index = page.rindex("39301")
  lines = page[index:].split("\n") if index != -1 else []
  rows = lines[0:4]

  for row in rows:
    match = pattern_material_fee().match(row)
    if match:
      code, groups_raw, fee_sml, fee_cop = match.groups()

      groups = [g.strip() for g in groups_raw.split("-") if g.strip()]

      for group in groups:
        records.append(
          {
            "code": int(code),
            "group": int(group),
            "Fee (S.M.L.D.V)": float(fee_sml.replace(",", ".")),
            "Fee (COP)": int(fee_cop.replace(".", "")),
          }
        )

  return pd.DataFrame(records)
