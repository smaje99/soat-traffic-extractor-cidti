from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Container, Singleton

from api.context.procedures.infrastructure import ProcedureContainer
from api.context.procedures.infrastructure.http import procedure_endpoints
from api.context.surgical_groups.infrastructure import SurgicalGroupContainer
from api.context.surgical_groups.infrastructure.http import surgical_group_endpoints
from api.database import get_database_connection


__all__ = ("ApplicationContainer",)


class ApplicationContainer(DeclarativeContainer):
  """Application IoC container."""

  wiring_config = WiringConfiguration(modules=[procedure_endpoints, surgical_group_endpoints])

  database = Singleton(get_database_connection)

  surgical_group = Container(SurgicalGroupContainer, database=database)

  procedure = Container(ProcedureContainer, database=database)
