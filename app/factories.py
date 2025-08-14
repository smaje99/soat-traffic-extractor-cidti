from typing import final

from app.services import ProcedureService, SurgeonService


__all__ = ("ServiceFactory",)


@final
class ServiceFactory:
  """Factory for creating service instances."""
  def __init__(self) -> None:
    """Initialize the service factory."""
    self.__procedure = ProcedureService()
    self.__surgeon = SurgeonService()

  @property
  def procedure(self) -> ProcedureService:
    """Get the ProcedureService singleton instance."""
    return self.__procedure

  @property
  def surgeon(self) -> SurgeonService:
    """Get the SurgicalProfessionalService singleton instance."""
    return self.__surgeon
