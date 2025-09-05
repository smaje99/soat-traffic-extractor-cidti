import math
from typing import Annotated, Final

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


__all__ = (
    "Group",
    "Code",
    "Procedure",
    "FeeBase",
    "Fee",
    "PreConsultationFee",
    "MaterialFee",
)


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

MIN_CODE_PROCEDURE_LENGTH: Final = 4
MAX_CODE_PROCEDURE_LENGTH: Final = 5

MODEL_CONFIG: Final = ConfigDict(from_attributes=True)


def validate_group(group: int | str) -> int:
  """Validate group procedure number."""
  if isinstance(group, str):
    group = int(group)

  if group not in ALLOWED_GROUPS:
    raise ValueError("Group must be between 2 and 23.")
  return group


Group = Annotated[int, BeforeValidator(validate_group)]
"""Value Object for Group Procedure."""


def validate_code(code: int | str) -> int:
  """Validate code procedure number."""
  if isinstance(code, str):
    code = int(code)

  digits = int(math.log10(code)) + 1 if code > 0 else 0
  if not (MIN_CODE_PROCEDURE_LENGTH <= digits <= MAX_CODE_PROCEDURE_LENGTH):
    raise ValueError("Code must be between 4 and 5 digits.")
  return code

Code = Annotated[int, BeforeValidator(validate_code)]
"""Value Object for Code Procedure."""


class Procedure(BaseModel):
  """Procedure schema."""

  code: Code
  """Code procedure. Must be between 4 and 5 digits."""
  group: Group

  model_config = MODEL_CONFIG


class FeeBase(BaseModel):
  """Base schema for fees."""

  code: int
  fee_sml: float = Field(..., alias="Fee (S.M.L.D.V)")
  fee_cop: float = Field(..., alias="Fee (COP)")


class Fee(FeeBase):
  """Fee schema."""

  group: Group

  model_config = MODEL_CONFIG


class PreConsultationFee(BaseModel):
  """Pre-Consultation Fee schema."""

  description: str

  model_config = MODEL_CONFIG


class MaterialFee(BaseModel):
  """Material Fee schema."""

  group: Group

  model_config = MODEL_CONFIG


class SurgicalGroup(BaseModel):
  """Surgical Group schema."""

  group: Group
  special: bool
  surgeon: float = Field(..., alias="cirujano")
  anesthesiology: float = Field(..., alias="anestesiología")
  assistant: float = Field(..., alias="ayudantía")
  operating_room: float = Field(..., alias="sala de cirugía")
  materials: float = Field(..., alias="instrumentario")
  presurgical: float = Field(..., alias="prequirúrgica")
  preanesthetic: float = Field(..., alias="preanestésica")
  total: float

  model_config = MODEL_CONFIG
