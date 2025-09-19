from sqlite3 import Connection

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from api.context.surgical_groups.domain import SurgicalGroupRepository
from api.context.surgical_groups.infrastructure.http import SurgicalGroupGetController
from api.context.surgical_groups.infrastructure.persistence import (
  SQLiteSurgicalGroupDAO,
  SQLiteSurgicalGroupRepository,
)


__all__ = ("SurgicalGroupContainer",)


class SurgicalGroupContainer(DeclarativeContainer):
  """Dependency Injection container for Surgical Group module."""

  database = Dependency(instance_of=Connection)

  surgical_group_dao = Factory(SQLiteSurgicalGroupDAO, connection=database)

  surgical_group_repository: Factory[SurgicalGroupRepository] = Factory(SQLiteSurgicalGroupRepository, dao=surgical_group_dao)

  surgical_group_get_controller = Factory(SurgicalGroupGetController, repository=surgical_group_repository)
