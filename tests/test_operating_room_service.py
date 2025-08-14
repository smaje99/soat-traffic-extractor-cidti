from pandas import DataFrame
from pytest import approx  # type: ignore

from app.services import OperatingRoomService


def test_load_data():
  """Test loading data for the OperatingRoomService."""
  service = OperatingRoomService()
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
  service = OperatingRoomService()
  service.load_data()
  result = service.find_by_code(39209)
  print(service.data)

  assert not result.empty
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["group"].iloc[0] == 7  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(16.88, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 801000  # noqa: PLR2004


def test_find_by_code_not_found():
  """Test finding anesthesiologists by code when not found."""
  service = OperatingRoomService()
  service.load_data()
  result = service.find_by_code(99999)

  assert isinstance(result, DataFrame)
  assert result.empty


def test_find_by_special_code():
  """Test finding anesthesiologists by special code."""
  service = OperatingRoomService()
  service.load_data()
  result = service.find_by_code(39219)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["group"].iloc[0] == 23  # noqa: PLR2004
  assert result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(48.07, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == 2_280_900  # noqa: PLR2004


def test_find_by_group():
  """Test finding anesthesiologists by group."""
  service = OperatingRoomService()
  service.load_data()
  result = service.find_by_group(3)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["code"].iloc[0] == 39205  # noqa: PLR2004
  assert not result["special"].iloc[0]
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(5.97, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == int(round(5.97 * 47_450, -2))
