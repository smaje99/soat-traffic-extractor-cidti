from pytest import fixture
from app.services.procedure import ProcedureService


@fixture
def service_factory() -> ProcedureService:
    """Factory function to create a ProcedureService instance."""
    return ProcedureService()


def test_factory_create_procedure_service(service_factory: ProcedureService):
  """Test factory function for ProcedureService."""
  procedure_service = service_factory
  assert procedure_service is not None
  assert isinstance(procedure_service, ProcedureService)
