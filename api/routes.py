from typing import Annotated

from fastapi import APIRouter, Depends

from api.controllers.procedure import ProcedureGetResponse, get_procedure_controller
from api.data import get_factory
from api.schemas import Code

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
