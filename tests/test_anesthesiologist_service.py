from pandas import DataFrame
from pytest import approx  # type: ignore

from app.services import AnesthesiologistService


def test_load_data():
  """Test loading data for the AnesthesiologistService."""
  service = AnesthesiologistService()
  service.load_data()

  assert not service.data.empty
  assert len(service.data) == 16  # noqa: PLR2004
  assert list(service.data.columns) == [
    "code",
    "group",
    "special",
    "Fee (S.M.L.D.V)",
    "Fee (COP)",
  ]


def test_find_by_code():
  """Test finding anesthesiologists by code."""
  service = AnesthesiologistService()
  service.load_data()
  result = service.find_by_code(39110)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["group"].iloc[0] == 12  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(11.44, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 542800  # noqa: PLR2004


def test_find_by_code_not_found():
  """Test finding anesthesiologists by code when not found."""
  service = AnesthesiologistService()
  service.load_data()
  result = service.find_by_code(99999)

  assert isinstance(result, DataFrame)
  assert result.empty


def test_find_by_special_code():
  """Test finding anesthesiologists by special code."""
  service = AnesthesiologistService()
  service.load_data()
  result = service.find_by_code(39114)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["group"].iloc[0] == 22  # noqa: PLR2004
  assert result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(26.82, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 1_272_600  # noqa: PLR2004


def test_find_by_group():
  """Test finding anesthesiologists by group."""
  service = AnesthesiologistService()
  service.load_data()
  result = service.find_by_group(6)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["code"].iloc[0] == 39104  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(4.56, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == int(round(4.56 * 47_450, -2))
