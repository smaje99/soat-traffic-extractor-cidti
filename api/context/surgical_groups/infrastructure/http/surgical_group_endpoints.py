from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.context.surgical_groups.domain.objects import Group

from .surgical_group_dto import SurgicalGroupGetResponse
from .surgical_group_get_controller import SurgicalGroupGetController


router = APIRouter()


@router.get("/{group}")
@inject
def get_surgical_group(  # noqa: D417
  group: Group,
  *,
  controller: SurgicalGroupGetController = Depends(  # noqa: B008
    Provide["surgical_group.surgical_group_get_controller"]
  ),
) -> SurgicalGroupGetResponse:
  """Get surgical group by group.

  Args:
  * group (Group): The group of the surgical group to retrieve.

  Raises:
  * ValueError: If the group is not valid. HTTP 400.
  * HTTPException: If the surgical group is not found. HTTP 400.

  Returns:
  * SurgicalGroupGetResponse: The surgical group found.
  """
  return controller(group)
