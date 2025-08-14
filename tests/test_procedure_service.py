from pathlib import Path

from pandas import DataFrame
from pytest import MonkeyPatch, fixture

from app.services.procedure import ProcedureService


@fixture
def sample_data():
  """Fixture to provide sample data for testing."""
  return DataFrame(
    [
      {"code": "1001", "description": "Test Proc 1", "group": 10},
      {"code": "2002", "description": "Test Proc 2", "group": 20},
      {"code": "3003", "description": "Test Proc 3", "group": 20},
    ]
  )


@fixture
def patch_procedure_service(monkeypatch: MonkeyPatch, sample_data: DataFrame) -> MonkeyPatch:
  """Fixture to patch ProcedureService methods for testing."""
  def mock_extract_text(pdf_path: Path, page_start: int, page_end: int):
    return [
      "1001    Test Proc 1    10",
      "2002    Test Proc 2    20",
      "3003    Test Proc 3    20",
    ]

  def mock_parse_records(pages: list[str]):
    return sample_data

  monkeypatch.setattr("app.services.procedure.extract_text_from_pdf", mock_extract_text)
  monkeypatch.setattr(
    "app.services.procedure.parse_procedure_records", mock_parse_records
  )

  return monkeypatch


def test_load_data(patch_procedure_service: MonkeyPatch, sample_data: DataFrame):
  """Test loading data with monkey patching."""
  procedure = ProcedureService()
  procedure.load_data()

  assert not procedure.data.empty
  assert len(procedure.data) == len(sample_data)

def test_load_data_real():
  """Test loading data without monkey patching."""
  procedure = ProcedureService()
  procedure.load_data()

  assert not procedure.data.empty
  assert len(procedure.data) == 1771
  assert list(procedure.data.columns) == ["code", "group"]
  assert len(procedure.data["group"].unique()) == 16  # noqa: PLR2004

def test_find_by_code():
  """Test finding procedures by code."""
  procedure = ProcedureService()
  procedure.load_data()
  result = procedure.find_by_code(1101)

  assert result is not None
  assert isinstance(result, DataFrame)
  assert len(result) == 1
  assert result["group"].iloc[0] == 9  # noqa: PLR2004
