from pathlib import Path
from typing import Any

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
  assert len(procedure.data["group"].unique()) == 16

def test_find_by_code(patch_procedure_service: MonkeyPatch, sample_data: DataFrame):
  """Test finding procedures by code."""
  procedure = ProcedureService()
  procedure.load_data()

def test_export_to_csv(patch_procedure_service: MonkeyPatch, sample_data: DataFrame):
  """Test exporting data to CSV."""
  export_to_csv_dict = {"called": False}

  def mock_export_to_csv(_: Any, output_path: Path):
    export_to_csv_dict["called"] = True

  patch_procedure_service.setattr("app.services.procedure.export_to_csv", mock_export_to_csv)

  procedure = ProcedureService()
  procedure.load_data()
  procedure.export_to_csv(Path("output.csv"))

  assert export_to_csv_dict["called"]

def test_export_to_json(patch_procedure_service: MonkeyPatch, sample_data: DataFrame):
  """Test exporting data to JSON."""
  export_to_json_dict = {"called": False}

  def mock_export_to_json(_: Any, output_path: Path):
    export_to_json_dict["called"] = True

  patch_procedure_service.setattr("app.services.procedure.export_to_json", mock_export_to_json)

  procedure = ProcedureService()
  procedure.load_data()
  procedure.export_to_json(Path("output.json"))

  assert export_to_json_dict["called"]
