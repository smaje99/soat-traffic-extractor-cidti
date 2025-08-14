from typing import final

from app.services import ProcedureService, SurgicalProfessionalService


__all__ = ("ServiceFactory",)


@final
class ServiceFactory:
  """Factory for creating service instances."""
  def __init__(self) -> None:
    """Initialize the service factory."""
    self.__procedure = ProcedureService()
    self.__surgical_professional = SurgicalProfessionalService()

  @property
  def procedure(self) -> ProcedureService:
    """Get the ProcedureService singleton instance."""
    return self.__procedure

  @property
  def surgical_professional(self) -> SurgicalProfessionalService:
    """Get the SurgicalProfessionalService singleton instance."""
    return self.__surgical_professional
