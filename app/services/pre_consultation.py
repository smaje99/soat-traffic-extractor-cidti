from pathlib import Path
from typing import Final, final, override

from pandas import DataFrame

from app.exporter import export_to_csv, export_to_json
from app.extractor import extract_text_from_pdf
from app.interfaces import ExportDataInterface, FinderByCodeInterface
from app.parser import parse_pre_consultation_fees
from app.services.service import ServiceABC


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 98
FINAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 99


@final
class PreConsultationService(ServiceABC, ExportDataInterface, FinderByCodeInterface):
  """Service for managing pre consultation fees."""

  def __init__(self):
    """Service for managing pre consultation fees."""
    super().__init__()

  @override
  def load_data(self):
    """Load pre consultation fees data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_DOCUMENT,
      FINAL_NUMBER_PAGE_FROM_DOCUMENT,
    )
    self._data = parse_pre_consultation_fees(pages)

  @override
  def find_by_code(self, code: int) -> DataFrame:
    """Find a row by code."""
    return self._data[self._data["code"] == code]

  @override
  def export_to_csv(self, output_path: Path) -> None:
    """Export data to a CSV file."""
    export_to_csv(self._data, output_path)

  @override
  def export_to_json(self, output_path: Path) -> None:
    """Export data to a JSON file."""
    export_to_json(self._data, output_path)
