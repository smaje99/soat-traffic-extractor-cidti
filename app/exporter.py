from pathlib import Path

import pandas as pd

from app.database import get_database


__all__ = ("export_to_csv", "export_to_json",)


def _create_output_folder(input_path: Path):
    """Create the output folder if it doesn't exist."""
    input_path.parent.mkdir(parents=True, exist_ok=True)


def export_to_csv(df: pd.DataFrame, output_path: Path):
  """Export DataFrame to CSV file.

  Args:
      df (pd.DataFrame): The DataFrame to export.
      output_path (Path): The path to the output CSV file.
      columns (list[str]): The columns to export.
  """
  _create_output_folder(output_path)
  df.to_csv(output_path, index=False, encoding="utf-8-sig")


def export_to_json(df: pd.DataFrame, output_path: Path):
  """Export DataFrame to JSON file.

  Args:
      df (pd.DataFrame): The DataFrame to export.
      output_path (Path): The path to the output JSON file.
  """
  _create_output_folder(output_path)
  df.to_json(output_path, orient="records", indent=2, force_ascii=False)  # type: ignore


def export_to_sqlite(df: pd.DataFrame, table_name: str):
  """Export DataFrame to SQLite database.

  Args:
      df (pd.DataFrame): The DataFrame to export.
      table_name (str): The name of the table to export the data to.
  """
  df.to_sql(table_name, get_database(), if_exists="replace", index=False)  # type: ignore
