from pathlib import Path
from typing import Final, final

from pandas import DataFrame

from app.exporter import export_to_csv, export_to_json
from app.extractor import extract_text_from_pdf
from app.parser import parse_procedure_records


__all__ = ("ProcedureService",)


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_CHAPTER_TREE: Final = 2
FINAL_NUMBER_PAGE_FROM_CHAPTER_TREE: Final = 62


@final
class ProcedureService:
  """Service for managing procedures in the SOAT 2025 tariff."""
  def __init__(self):
    """Service for managing procedures in the SOAT 2025 tariff."""

  def load_data(self):
    """Load procedure data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_CHAPTER_TREE,
      FINAL_NUMBER_PAGE_FROM_CHAPTER_TREE
    )
    self.__data = parse_procedure_records(pages)

  @property
  def data(self) -> DataFrame:
    """Get the procedure data."""
    return self.__data

  def export_to_csv(self, output_path: Path):
    """Export the procedure data to a CSV file."""
    export_to_csv(self.__data, output_path)

  def export_to_json(self, output_path: Path):
    """Export the procedure data to a JSON file."""
    export_to_json(self.__data, output_path)

  def find_by_code(self, code: int) -> DataFrame:
    """Find a procedure by its code."""
    return self.__data[self.__data["code"] == code]
