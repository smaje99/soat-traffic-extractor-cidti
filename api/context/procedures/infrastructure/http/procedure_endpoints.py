from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.context.procedures.domain.objects import Code

from .procedure_dto import ProcedureGetResponse
from .procedure_get_controller import ProcedureGetController


router = APIRouter()


@router.get("/procedures/{code}")
@inject
def get_procedure(  # noqa: D417
  code: Code,
  *,
  controller: ProcedureGetController = Depends(  # noqa: B008
    Provide["procedure.procedure_get_controller"]
  ),
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
  return controller(code)
