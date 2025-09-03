from typing import Annotated, Final

from pydantic import BaseModel, BeforeValidator, Field


ALLOWED_GROUPS: Final[list[int]] = [
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  20,
  21,
  22,
  23,
]


def validate_group(group: int) -> int:
  """Validate group procedure number."""
  if group not in ALLOWED_GROUPS:
    raise ValueError("Group must be between 2 and 23.")
  return group


Group = Annotated[int, BeforeValidator(validate_group)]
"""Value Object for Group Procedure."""


class Procedure(BaseModel):
  """Procedure schema."""

  code: int = Field(..., gt=999, lt=100000)
  """Code procedure. Must be between 4 and 5 digits."""
  group: Group


class FeeBase(BaseModel):
  """Base schema for fees."""

  code: int
  fee_sml: float = Field(..., alias="Fee (S.M.L.D.V)")
  fee_cop: float = Field(..., alias="Fee (COP)")


class Fee(FeeBase):
  """Fee schema."""

  group: Group


class PreConsultationFee(BaseModel):
  """Pre-Consultation Fee schema."""

  description: str


class MaterialFee(BaseModel):
  """Material Fee schema."""

  group: Group
