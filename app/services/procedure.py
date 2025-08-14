from pathlib import Path
from typing import Final, final

from app.extractor import extract_text_from_pdf
from app.parser import parse_procedure_records
from app.services.service import ServiceBase


__all__ = ("ProcedureService",)


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_CHAPTER_TREE: Final = 2
FINAL_NUMBER_PAGE_FROM_CHAPTER_TREE: Final = 62


@final
class ProcedureService(ServiceBase):
  """Service for managing procedures in the SOAT 2025 tariff."""
  def __init__(self):
    """Service for managing procedures in the SOAT 2025 tariff."""
    super().__init__()

  def load_data(self):
    """Load procedure data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_CHAPTER_TREE,
      FINAL_NUMBER_PAGE_FROM_CHAPTER_TREE,
    )
    self._data = parse_procedure_records(pages)
