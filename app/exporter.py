from pathlib import Path

import pandas as pd


__all__ = ("export_to_csv", "export_to_json",)


def export_to_csv(df: pd.DataFrame, output_path: Path):
  """Export DataFrame to CSV file.

  Args:
      df (pd.DataFrame): The DataFrame to export.
      output_path (Path): The path to the output CSV file.
      columns (list[str]): The columns to export.
  """
  df.to_csv(output_path, index=False, encoding="utf-8-sig")


def export_to_json(df: pd.DataFrame, output_path: Path):
  """Export DataFrame to JSON file.

  Args:
      df (pd.DataFrame): The DataFrame to export.
      output_path (Path): The path to the output JSON file.
  """
  df.to_json(output_path, orient="records", indent=2, force_ascii=False)  # type: ignore
