from pathlib import Path
from typing import Final, final

from app.extractor import extract_text_from_pdf
from app.parser import parse_pre_consultation_fees
from app.services.service import ServiceBase


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 98
FINAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 99


@final
class PreConsultationService(ServiceBase):
  """Service for managing pre consultation fees."""

  def __init__(self):
    """Service for managing pre consultation fees."""
    super().__init__()

  def load_data(self):
    """Load pre consultation fees data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_DOCUMENT,
      FINAL_NUMBER_PAGE_FROM_DOCUMENT,
    )
    self._data = parse_pre_consultation_fees(pages)
