from sqlite3 import Connection

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from api.context.procedures.domain import ProcedureRepository
from api.context.procedures.infrastructure.http import ProcedureGetController
from api.context.procedures.infrastructure.persistence import (
  SQLiteProcedureDAO,
  SQLiteProcedureRepository,
)


__all__ = ("ProcedureContainer",)


class ProcedureContainer(DeclarativeContainer):
  """Dependency Injection container for Procedure module."""

  database = Dependency(instance_of=Connection)

  procedure_dao = Factory(SQLiteProcedureDAO, connection=database)

  procedure_repository: Factory[ProcedureRepository] = Factory(
    SQLiteProcedureRepository, dao=procedure_dao
  )

  procedure_get_controller = Factory(
    ProcedureGetController, repository=procedure_repository
  )
