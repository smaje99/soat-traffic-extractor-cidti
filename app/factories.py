from typing import final

from app.services.procedure import ProcedureService


__all__ = ("ServiceFactory",)


@final
class ServiceFactory:
  """Factory for creating service instances."""
  def __init__(self) -> None:
    """Initialize the service factory."""
    self.__procedure: ProcedureService = ProcedureService()

  @property
  def procedure(self) -> ProcedureService:
    """Get the ProcedureService singleton instance."""
    return self.__procedure
