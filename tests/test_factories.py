import pytest

from app.factories import ServiceFactory
from app.services import (
  AnesthesiologistService,
  AssistantService,
  MaterialService,
  OperatingRoomService,
  PreConsultationService,
  ProcedureService,
  SurgeonService,
)


@pytest.fixture
def service_factory():
  """Fixture for creating service instances."""
  return ServiceFactory()


def test_factory_create_procedure_service(service_factory: ServiceFactory):
  """Test factory function for ProcedureService."""
  procedure_service = service_factory.procedure
  assert procedure_service is not None
  assert isinstance(procedure_service, ProcedureService)


def test_factory_create_surgeon_service(service_factory: ServiceFactory):
  """Test factory function for SurgeonService."""
  surgeon_service = service_factory.surgeon
  assert surgeon_service is not None
  assert isinstance(surgeon_service, SurgeonService)


def test_factory_create_anesthesiologist_service(service_factory: ServiceFactory):
  """Test factory function for AnesthesiologistService."""
  anesthesiologist_service = service_factory.anesthesiologist
  assert anesthesiologist_service is not None
  assert isinstance(anesthesiologist_service, AnesthesiologistService)


def test_factory_create_assistant_service(service_factory: ServiceFactory):
  """Test factory function for AssistantService."""
  assistant_service = service_factory.assistant
  assert assistant_service is not None
  assert isinstance(assistant_service, AssistantService)


def test_factory_create_pre_consultation_service(service_factory: ServiceFactory):
  """Test factory function for PreConsultationService."""
  pre_consultation_service = service_factory.pre_consultation
  assert pre_consultation_service is not None
  assert isinstance(pre_consultation_service, PreConsultationService)


def test_factory_create_operating_room_service(service_factory: ServiceFactory):
  """Test factory function for OperatingRoomService."""
  operating_room_service = service_factory.operating_room
  assert operating_room_service is not None
  assert isinstance(operating_room_service, OperatingRoomService)


def test_factory_create_material_service(service_factory: ServiceFactory):
  """Test factory function for MaterialService."""
  material_service = service_factory.material
  assert material_service is not None
  assert isinstance(material_service, MaterialService)
