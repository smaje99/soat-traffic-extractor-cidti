from pydantic import BaseModel, Field

from api.context.procedures.domain import Procedure
from api.context.surgical_groups.domain import SurgicalGroup


__all__ = ("ProcedureGetResponse",)


class ProcedureGetResponse(BaseModel):
  """Response schema for getting a procedure by code."""

  procedure: Procedure
  """The procedure found by code."""
  surgical_group: SurgicalGroup = Field(..., alias="surgicalGroup")
  """The surgical group associated with the procedure."""
