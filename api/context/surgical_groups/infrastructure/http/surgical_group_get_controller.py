from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from api.context.surgical_groups.domain import SurgicalGroupRepository
from api.context.surgical_groups.domain.objects import Group

from .surgical_group_dto import SurgicalGroupGetResponse


__all__ = ("SurgicalGroupGetController",)


class SurgicalGroupGetController:
  """Controller for getting a surgical group by its group."""

  def __init__(self, repository: SurgicalGroupRepository,):
    """Initialize the controller with the surgical group repository."""
    self.__repository = repository

  def __call__(self, group: Group) -> SurgicalGroupGetResponse:
    """Get a surgical group by its group.

    Args:
        group (Group): The group of the surgical group to retrieve.

    Returns:
        SurgicalGroup: The surgical group associated with the given group.

    Raises:
        ValueError: If no surgical group is found with the given group.
    """
    surgical_group_record = self.__repository.find(group)
    if surgical_group_record is None:
      raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST, detail="Surgical group not found"
      )

    return SurgicalGroupGetResponse.model_validate(surgical_group_record)
