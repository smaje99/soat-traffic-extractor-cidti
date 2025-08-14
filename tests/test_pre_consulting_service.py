from pandas import DataFrame
from pytest import approx  # type: ignore

from app.services import PreConsultationService


def test_load_data():
  """Test loading data for the PreConsultationService."""
  service = PreConsultationService()
  service.load_data()

  assert not service.data.empty
  assert len(service.data) == 2  # noqa: PLR2004
  assert list(service.data.columns) == [
    "code",
    "description",
    "Fee (S.M.L.D.V)",
    "Fee (COP)",
  ]
  assert list(service.data["code"]) == [39137, 39139]


def test_find_by_code():
  """Test finding anesthesiologists by code."""
  service = PreConsultationService()
  service.load_data()
  result = service.find_by_code(39137)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(1.48, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == int(round(1.48 * 47_450, -2))  # noqa: PLR2004


def test_find_by_code_not_found():
  """Test finding anesthesiologists by code when not found."""
  service = PreConsultationService()
  service.load_data()
  result = service.find_by_code(99999)

  assert isinstance(result, DataFrame)
  assert result.empty
