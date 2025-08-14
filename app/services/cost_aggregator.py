from pathlib import Path
from typing import Final, cast, final, override

from pandas import DataFrame

from app.exporter import export_to_csv, export_to_json
from app.interfaces import ExportDataInterface, FinderByGroupInterface
from app.services.pre_consultation import PreConsultationService
from app.services.service import ServiceABC


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
    """Load and aggregate fee data for all surgical groups.

    This method iterates through all surgical groups and their "special" flags,
    collecting fees from multiple service finders (e.g., surgeon, anesthesiologist,
    materials) and pre-consultation data. For each group:
      - Initializes a record containing the group identifier and special flag.
      - Collects fees from each registered group finder service, summing them
        into a running total for the group.
      - Adds pre-consultation fees unless the group is listed in
        `GROUPS_NO_PRE_CONSULTING`.
      - Appends the total cost and stores the record in a list.

    Once all groups have been processed, the list of records is converted into a
    pandas DataFrame and stored in `self._data`.

    Side Effects:
        Updates the internal `_data` attribute with the aggregated results.
    """
    records: list[dict[str, int | str | bool]] = []
    pre_consultation_data = self.__pre_consulting.data
    pre_consultation_columns = self.__pre_consulting.column_list

    # Iterate through each group and its "special" flag
    for group, is_special in zip(self.__groups, self.__special_groups, strict=False):
      record: dict[str, int | str | bool] = {"group": group, "special": is_special}
      total: int = 0

      # Collect fees from each service finder for the current group
      for finder in self.__group_finders:
        data = finder.find_by_group(group)
        fee = data["Fee (COP)"].iloc[0] if not data.empty else 0
        service: ServiceABC = cast(ServiceABC, finder)
        record[service.column] = fee
        total += fee

      # Add pre-consultation fees if applicable
      for index, column_name in enumerate(pre_consultation_columns):
        fee = (
          pre_consultation_data["Fee (COP)"].iloc[index]
          if group not in GROUPS_NO_PRE_CONSULTING
          else 0
        )
        record[column_name] = fee
        total += fee

      # Store the total cost for the group
      record["total"] = total
      records.append(record)

    # Save aggregated results as a DataFrame
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

  @property
  @override
  def column(self) -> str:
    """Get the column name of the service."""
    return "costos"
