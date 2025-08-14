from pandas import DataFrame
from pytest import approx  # type: ignore

from app.services import SurgeonService


def test_load_data():
  """Test loading data for the SurgeonService."""
  service = SurgeonService()
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
  service = SurgeonService()
  service.load_data()
  result = service.find_by_code(39000)

  assert isinstance(result, DataFrame)
  assert not result.empty
  assert len(result) == 1
  assert result["group"].iloc[0] == 2  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(2.93, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 139000  # noqa: PLR2004


def test_find_by_code_not_found():
  """Test finding anesthesiologists by code when not found."""
  service = SurgeonService()
  service.load_data()
  result = service.find_by_code(99999)

  assert isinstance(result, DataFrame)
  assert result.empty


def test_find_by_special_code():
  """Test finding anesthesiologists by special code."""
  service = SurgeonService()
  service.load_data()
  result = service.find_by_code(39012)

  assert isinstance(result, DataFrame)
  assert not result.empty
  assert len(result) == 1
  assert result["group"].iloc[0] == 20  # noqa: PLR2004
  assert result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(25.43, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 1_206_700  # noqa: PLR2004


def test_find_by_group():
  """Test finding anesthesiologists by group."""
  service = SurgeonService()
  service.load_data()
  result = service.find_by_group(8)

  assert isinstance(result, DataFrame)
  assert not result.empty
  assert len(result) == 1
  assert result["code"].iloc[0] == 39006  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(10.44, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == int(round(10.44 * 47_450, -2))
