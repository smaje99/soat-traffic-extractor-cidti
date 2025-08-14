import pytest

from app.factories import ServiceFactory
from app.services import CostAggregatorService


factory = ServiceFactory()


@pytest.fixture
def cost_aggregator_service():
  """Fixture for CostAggregatorService."""
  return factory.cost_aggregator


def test_load_data(cost_aggregator_service: CostAggregatorService):
  """Test loading data for the CostAggregatorService."""
  assert not cost_aggregator_service.data.empty
  assert len(cost_aggregator_service.data) == 16  # noqa: PLR2004
  assert list(cost_aggregator_service.data.columns) == [
    "group",
    "special",
    "cirujano",
    "anestesiología",
    "ayudantía",
    "sala de cirugía",
    "instrumentario",
    "prequirúrgica",
    "preanestésica",
    "total"
  ]


def test_find_by_group(cost_aggregator_service: CostAggregatorService):
  """Test finding cost aggregation by group."""
  result = cost_aggregator_service.find_by_group(9)

  assert not result.empty
  assert len(result) == 1
  assert not result["special"].iloc[0]  # noqa: PLR2004
  assert result["cirujano"].iloc[0] == 605500  # noqa: PLR2004
  assert result["anestesiología"].iloc[0] == 346400  # noqa: PLR2004
  assert result["ayudantía"].iloc[0] == 165600  # noqa: PLR2004
  assert result["sala de cirugía"].iloc[0] == 1_001_200  # noqa: PLR2004
  assert result["instrumentario"].iloc[0] == 470700  # noqa: PLR2004
  assert result["prequirúrgica"].iloc[0] == 70200  # noqa: PLR2004
  assert result["preanestésica"].iloc[0] == 70200  # noqa: PLR2004
  assert result["total"].iloc[0] == 2_729_800  # noqa: PLR2004


def test_find_by_group_not_found(cost_aggregator_service: CostAggregatorService):
  """Test finding cost aggregation by group not found."""
  result = cost_aggregator_service.find_by_group(99)

  assert result.empty


def test_find_by_group_without_pre_consulting(cost_aggregator_service: CostAggregatorService):
  """Test finding cost aggregation by group without pre-consulting."""
  result = cost_aggregator_service.find_by_group(3)

  assert not result.empty
  assert len(result) == 1
  assert not result["special"].iloc[0]  # noqa: PLR2004
  assert result["cirujano"].iloc[0] == 169400  # noqa: PLR2004
  assert result["anestesiología"].iloc[0] == 120_000  # noqa: PLR2004
  assert result["ayudantía"].iloc[0] == 0  # noqa: PLR2004
  assert result["sala de cirugía"].iloc[0] == 283300  # noqa: PLR2004
  assert result["instrumentario"].iloc[0] == 108200  # noqa: PLR2004
  assert result["prequirúrgica"].iloc[0] == 0  # noqa: PLR2004
  assert result["preanestésica"].iloc[0] == 0  # noqa: PLR2004
  assert result["total"].iloc[0] == 680900  # noqa: PLR2004
