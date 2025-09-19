from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from api.context.procedures.domain import Procedure, ProcedureRepository
from api.context.procedures.domain.objects import Code
from api.context.surgical_groups.domain import SurgicalGroup, SurgicalGroupRepository

from .procedure_dto import ProcedureGetResponse


__all__ = ("ProcedureGetController",)


class ProcedureGetController:
  """Controller for getting a procedure by its code."""

  def __init__(
    self,
    procedure_repository: ProcedureRepository,
    surgical_group_repository: SurgicalGroupRepository,
  ):
    """Initialize the controller with the procedure repository."""
    self.__procedure_repository = procedure_repository
    self.__surgical_group_repository = surgical_group_repository

  def __call__(self, code: Code) -> ProcedureGetResponse:
    """Get a procedure by its code.

    Args:
        code (Code): The code of the procedure to retrieve.

    Returns:
        Procedure: The procedure associated with the given code.

    Raises:
        ValueError: If no procedure is found with the given code.
    """
    procedure_record = self.__procedure_repository.find(code)
    if procedure_record is None:
      raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Procedure not found")

    procedure = Procedure.model_validate(procedure_record)
    surgical_group_record = self.__surgical_group_repository.find(procedure.group)
    if surgical_group_record is None:
      raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST, detail="Surgical group not found"
      )

    surgical_group = SurgicalGroup.model_validate(surgical_group_record)
    return ProcedureGetResponse.model_validate({
      "procedure": procedure,
      "surgicalGroup": surgical_group
    })
