from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


__all__ = ("value_error_handler",)


def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
  """Handle ValueError exceptions and return a 400 Bad Request response."""
  return JSONResponse(
    status_code=HTTP_400_BAD_REQUEST,
    content={"detail": str(exc)},
  )
