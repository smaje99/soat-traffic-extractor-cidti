from fastapi import HTTPException
from pydantic import BaseModel, Field
from starlette.status import HTTP_400_BAD_REQUEST

from api.schemas import Code, Procedure, SurgicalGroup

from app.factories import ServiceFactory


__all__ = ("get_procedure_controller", "ProcedureGetResponse",)


class ProcedureGetResponse(BaseModel):
  """Response schema for getting a procedure by code."""

  procedure: Procedure
  """The procedure found by code."""
  surgical_group: SurgicalGroup = Field(..., alias="surgicalGroup")
  """The surgical group associated with the procedure."""


def get_procedure_controller(code: Code, factory: ServiceFactory) -> ProcedureGetResponse:
  """Get procedure by code."""
  procedure_df = factory.procedure.find_by_code(code)
  if procedure_df.empty:
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Procedure not found")
  procedure = Procedure.model_validate(procedure_df.iloc[0])

  surgical_group_df = factory.cost_aggregator.find_by_group(procedure.group)
  if surgical_group_df.empty:
    raise HTTPException(
      status_code=HTTP_400_BAD_REQUEST, detail="Surgical group not found"
    )
  surgical_group = SurgicalGroup.model_validate(surgical_group_df.iloc[0])

  return ProcedureGetResponse(
    procedure=procedure, surgicalGroup=surgical_group
  )
