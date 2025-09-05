from typing import Annotated

from fastapi import APIRouter, Depends

from api.controllers.procedure import ProcedureGetResponse, get_procedure_controller
from api.controllers.surgical_group import (
  SurgicalGroupGetResponse,
  get_surgical_group_controller,
)
from api.data import get_factory
from api.schemas import Code, Group

from app.factories import ServiceFactory


api_router = APIRouter()

FactoryDependency = Annotated[ServiceFactory, Depends(get_factory)]


@api_router.get("/procedures/{code}")
def get_procedure(  # noqa: D417
  code: Code, *, factory: FactoryDependency
) -> ProcedureGetResponse:
  """Get procedure by code.

  Args:
  * code (Code): The code of the procedure to retrieve.

  Raises:
  * ValueError: If the code is not length between 4 and 5 digits. HTTP 400.
  * HTTPException: If the procedure or surgical group is not found. HTTP 400.

  Returns:
  * ProcedureGetResponse: The procedure and surgical group found.
  """
  return get_procedure_controller(code, factory)


@api_router.get("/surgical-groups/{group}")
def get_surgical_group(  # noqa: D417
  group: Group, *, factory: FactoryDependency
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
  return get_surgical_group_controller(group, factory)
