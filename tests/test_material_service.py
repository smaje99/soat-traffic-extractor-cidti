from pandas import DataFrame
from pytest import approx  # type: ignore

from app.services import MaterialService


def test_load_data():
  """Test loading data for the MaterialService."""
  service = MaterialService()
  service.load_data()

  assert not service.data.empty
  assert len(service.data) == 12  # noqa: PLR2004
  assert list(service.data.columns) == [
    "code",
    "group",
    "Fee (S.M.L.D.V)",
    "Fee (COP)",
  ]


def test_find_by_code():
  """Test finding anesthesiologists by code."""
  service = MaterialService()
  service.load_data()
  result = service.find_by_code(39302)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 3  # noqa: PLR2004
  assert result["group"][3] == 5  # noqa: PLR2004
  assert result["Fee (S.M.L.D.V)"][3] == approx(4.27, rel=1e-3)
  assert result["Fee (COP)"][3] == 202600  # noqa: PLR2004


def test_find_by_code_not_found():
  """Test finding anesthesiologists by code when not found."""
  service = MaterialService()
  service.load_data()
  result = service.find_by_code(99999)

  assert isinstance(result, DataFrame)
  assert result.empty


def test_find_by_group():
  """Test finding anesthesiologists by group."""
  service = MaterialService()
  service.load_data()
  result = service.find_by_group(12)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["code"].iloc[0] == 39304  # noqa: PLR2004
  assert result["Fee (S.M.L.D.V)"].iloc[0] == approx(15.72, rel=1e-3)
  assert result["Fee (COP)"].iloc[0] == int(round(15.72 * 47_450, -2))
