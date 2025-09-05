from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from api.daos import get_surgical_group_dao
from api.schemas import Group, SurgicalGroup

from app.factories import ServiceFactory


__all__ = (
  "get_surgical_group_controller",
  "SurgicalGroupGetResponse",
)


class SurgicalGroupGetResponse(SurgicalGroup):
  """Response schema for Surgical Group."""


def get_surgical_group_controller(
  group: Group, factory: ServiceFactory
) -> SurgicalGroupGetResponse:
  """Get surgical group controller by group."""
  surgical_group_df = factory.cost_aggregator.find_by_group(group)
  if surgical_group_df.empty:
    raise HTTPException(
      status_code=HTTP_400_BAD_REQUEST, detail="Surgical group not found"
    )
  surgical_group = SurgicalGroupGetResponse.model_validate(
    get_surgical_group_dao(surgical_group_df)
  )

  return surgical_group
