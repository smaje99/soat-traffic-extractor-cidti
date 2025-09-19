import math
from typing import Annotated, Final

from pydantic import BeforeValidator


__all__ = ("Code",)


MIN_CODE_PROCEDURE_LENGTH: Final = 4
MAX_CODE_PROCEDURE_LENGTH: Final = 5


def validate_code(code: int | str) -> int:
  """Validate code procedure number."""
  if isinstance(code, str):
    code = int(code)

  digits = int(math.log10(code)) + 1 if code > 0 else 0
  if not (MIN_CODE_PROCEDURE_LENGTH <= digits <= MAX_CODE_PROCEDURE_LENGTH):
    raise ValueError("Code must be between 4 and 5 digits.")
  return code


Code = Annotated[int, BeforeValidator(validate_code)]  # noqa: F821
"""Value Object for Code Procedure."""
