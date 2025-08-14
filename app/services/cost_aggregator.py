from pathlib import Path
from typing import Final, cast, final, override

from pandas import DataFrame

from app.exporter import export_to_csv, export_to_json
from app.interfaces import ExportDataInterface, FinderByGroupInterface
from app.services.pre_consultation import PreConsultationService
from app.services.service import ServiceABC, ServiceBase


__all__ = ("CostAggregatorService",)


GROUPS_NO_PRE_CONSULTING: Final = [2, 3]
"""Those groups do not require pre-consultation according to
the article 75."""


@final
class CostAggregatorService(ServiceABC, FinderByGroupInterface, ExportDataInterface):
  """Service for aggregating costs from different surgical procedures groups."""

  def __init__(
    self,
    groups: list[int],
    special_groups: list[bool],
    group_finders: list[FinderByGroupInterface],
    pre_consulting: PreConsultationService,
  ):
    """Initialize the cost aggregator service."""
    super().__init__()
    self.__groups = groups
    self.__special_groups = special_groups
    self.__group_finders = group_finders
    self.__pre_consulting = pre_consulting

  @override
  def load_data(self):
    records: list[dict[str, int | str | bool]] = []

    for group, is_special in zip(self.__groups, self.__special_groups, strict=False):
      record: dict[str, int | str | bool] = {"group": group, "special": is_special}
      total: int = 0

      for finder in self.__group_finders:
        data = finder.find_by_group(group)
        fee = data["Fee (COP)"].iloc[0] if not data.empty else 0
        service: ServiceBase = cast(ServiceBase, finder)
        record[service.column] = fee
        total += fee

      pre_consultation_data = self.__pre_consulting.data
      pre_consultation_columns = self.__pre_consulting.column_list
      for index, column_name in enumerate(pre_consultation_columns):
        fee = (
          pre_consultation_data["Fee (COP)"].iloc[index]
          if group not in GROUPS_NO_PRE_CONSULTING
          else 0
        )
        record[column_name] = fee
        total += fee

      record["total"] = total
      records.append(record)

    self._data = DataFrame(records)

  @override
  def find_by_group(self, group: int) -> DataFrame:
    return self._data[self._data["group"] == group]

  @override
  def export_to_csv(self, output_path: Path):
    """Export the data to a CSV file."""
    export_to_csv(self._data, output_path)

  @override
  def export_to_json(self, output_path: Path):
    """Export the data to a JSON file."""
    export_to_json(self._data, output_path)
