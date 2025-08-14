from pathlib import Path
from typing import Final, final

from app.extractor import extract_text_from_pdf
from app.parser import parse_material_fees
from app.services.service import ServiceBase


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 100
FINAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 101


@final
class MaterialService(ServiceBase):
  """Service for managing material fees."""

  def __init__(self):
    """Service for managing material fees."""
    super().__init__()

  def load_data(self):
    """Load material fees data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_DOCUMENT,
      FINAL_NUMBER_PAGE_FROM_DOCUMENT,
    )
    self._data = parse_material_fees(pages)
