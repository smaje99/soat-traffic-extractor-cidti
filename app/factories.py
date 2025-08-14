from typing import final

from app.services import (
  AnesthesiologistService,
  AssistantService,
  CostAggregatorService,
  MaterialService,
  OperatingRoomService,
  PreConsultationService,
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
    self.__pre_consultation = PreConsultationService()
    self.__operating_room = OperatingRoomService()
    self.__material = MaterialService()
    self.__cost_aggregator = CostAggregatorService(
      groups=self.__surgeon.data["group"].sort_values().tolist(),
      special_groups=self.__surgeon.data["special"].tolist(),
      group_finders=[
        self.__surgeon,
        self.__anesthesiologist,
        self.__assistant,
        self.__operating_room,
        self.__material,
      ],
      pre_consulting=self.__pre_consultation,
    )

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

  @property
  def pre_consultation(self) -> PreConsultationService:
    """Get the PreConsultationService singleton instance."""
    return self.__pre_consultation

  @property
  def operating_room(self) -> OperatingRoomService:
    """Get the OperatingRoomService singleton instance."""
    return self.__operating_room

  @property
  def material(self) -> MaterialService:
    """Get the MaterialService singleton instance."""
    return self.__material

  @property
  def cost_aggregator(self) -> CostAggregatorService:
    """Get the CostAggregatorService singleton instance."""
    return self.__cost_aggregator
