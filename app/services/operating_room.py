from pathlib import Path
from typing import Final, final, override

from app.extractor import extract_text_from_pdf
from app.parser import parse_operating_room_fees
from app.services.service import ServiceBase


SOAT_FILE_PATH: Final = Path("data/soat-traffic-2025.pdf")
INITIAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 99
FINAL_NUMBER_PAGE_FROM_DOCUMENT: Final = 100


@final
class OperatingRoomService(ServiceBase):
  """Service for managing operating room fees."""

  def __init__(self):
    """Service for managing operating room fees."""
    super().__init__()

  @override
  def load_data(self):
    """Load operating room fees data from the source."""
    pages = extract_text_from_pdf(
      SOAT_FILE_PATH,
      INITIAL_NUMBER_PAGE_FROM_DOCUMENT,
      FINAL_NUMBER_PAGE_FROM_DOCUMENT,
    )
    self._data = parse_operating_room_fees(pages)

  @property
  @override
  def column(self) -> str:
    """Get the column name of the service."""
    return "sala de cirugía"
