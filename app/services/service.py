from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import override

from pandas import DataFrame

from app.exporter import export_to_csv, export_to_json
from app.interfaces import (
  ExportDataInterface,
  FinderByCodeInterface,
  FinderByGroupInterface,
)


__all__ = ("ServiceBase", "ServiceABC")


class ServiceABC(metaclass=ABCMeta):
  """Abstract base class for services."""

  def __init__(self):
    """Initialize the service."""
    self._data = DataFrame()

  @abstractmethod
  def load_data(self):
    """Load data for the service."""
    ...

  @property
  def data(self) -> DataFrame:
    """Get the data for the service."""
    return self._data

  @property
  @abstractmethod
  def column(self) -> str:
    """Get the column name of the service."""
    ...


class ServiceBase(
  ServiceABC,
  ExportDataInterface,
  FinderByCodeInterface,
  FinderByGroupInterface,
  metaclass=ABCMeta,
):
  """Base class for services."""

  @override
  def export_to_csv(self, output_path: Path):
    """Export the data to a CSV file."""
    export_to_csv(self._data, output_path)

  @override
  def export_to_json(self, output_path: Path):
    """Export the data to a JSON file."""
    export_to_json(self._data, output_path)

  @override
  def find_by_code(self, code: int) -> DataFrame:
    """Find a row by code."""
    return self._data[self._data["code"] == code]

  @override
  def find_by_group(self, group: int) -> DataFrame:
    """Find rows by group."""
    return self._data[self._data["group"] == group]
