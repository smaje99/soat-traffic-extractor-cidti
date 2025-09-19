from abc import ABCMeta, abstractmethod
from pathlib import Path

from pandas import DataFrame


__all__ = ("ExportDataInterface", "FinderByCodeInterface", "FinderByGroupInterface", "SQLiteExportInterface")


class ExportDataInterface(metaclass=ABCMeta):
  """Interface for exporting data."""

  @abstractmethod
  def export_to_csv(self, output_path: Path):
    """Export data to a CSV file."""

  @abstractmethod
  def export_to_json(self, output_path: Path):
    """Export data to a JSON file."""


class FinderByCodeInterface(metaclass=ABCMeta):
  """Interface for finding data by code."""

  @abstractmethod
  def find_by_code(self, code: int) -> DataFrame:
    """Find a row by code."""


class FinderByGroupInterface(metaclass=ABCMeta):
  """Interface for finding data by group."""

  @abstractmethod
  def find_by_group(self, group: int) -> DataFrame:
    """Find rows by group."""


class SQLiteExportInterface(metaclass=ABCMeta):
  """Interface for exporting data to SQLite."""

  @abstractmethod
  def export_to_sqlite(self):
    """Export data to a SQLite database table."""
