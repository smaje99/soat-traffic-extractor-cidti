from typing import override

from api.context.surgical_groups.domain import SurgicalGroup, SurgicalGroupRepository
from api.context.surgical_groups.domain.objects import Group

from .sqlite_surgical_group_dao import SQLiteSurgicalGroupDAO


class SQLiteSurgicalGroupRepository(SurgicalGroupRepository):
  """SQLite implementation of the SurgicalGroupRepository."""

  def __init__(self, dao: SQLiteSurgicalGroupDAO):
    """Initialize the repository with a SQLiteSurgicalGroupDAO instance."""
    self.__dao = dao

  @override
  def contains(self, code: Group) -> bool:
    return self.__dao.exists(code)

  @override
  def find(self, code: Group) -> SurgicalGroup | None:
    surgical_group_record = self.__dao.search(code)
    if surgical_group_record is None:
      return None

    return SurgicalGroup.model_validate(surgical_group_record)
