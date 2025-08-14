from typing import final

from app.services import (
  AnesthesiologistService,
  AssistantService,
  ProcedureService,
  SurgeonService,
)


__all__ = ("ServiceFactory",)


@final
class ServiceFactory:
  """Factory for creating service instances."""

  def __init__(self) -> None:
    """Initialize the service factory."""
    self.__procedure = ProcedureService()
    self.__surgeon = SurgeonService()
    self.__anesthesiologist = AnesthesiologistService()
    self.__assistant = AssistantService()

  @property
  def procedure(self) -> ProcedureService:
    """Get the ProcedureService singleton instance."""
    return self.__procedure

  @property
  def surgeon(self) -> SurgeonService:
    """Get the SurgeonService singleton instance."""
    return self.__surgeon

  @property
  def anesthesiologist(self) -> AnesthesiologistService:
    """Get the AnesthesiologistService singleton instance."""
    return self.__anesthesiologist

  @property
  def assistant(self) -> AssistantService:
    """Get the AssistantService singleton instance."""
    return self.__assistant
