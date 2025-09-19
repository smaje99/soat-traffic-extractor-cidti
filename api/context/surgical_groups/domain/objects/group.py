from typing import Annotated, Final

from pydantic import BeforeValidator


__all__ = ("Group",)


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


def validate_group(group: int | str) -> int:
  """Validate group procedure number."""
  if isinstance(group, str):
    group = int(group)

  if group not in ALLOWED_GROUPS:
    raise ValueError("Group must be between 2 and 23.")
  return group


Group = Annotated[int, BeforeValidator(validate_group)]
"""Value Object for Group Procedure."""
