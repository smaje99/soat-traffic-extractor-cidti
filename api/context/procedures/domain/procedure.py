from pydantic import BaseModel, ConfigDict

from api.context.procedures.domain.objects import Code
from api.context.surgical_groups.domain.objects import Group


class Procedure(BaseModel):
  """Procedure entity."""

  code: Code
  """Code procedure. Must be between 4 and 5 digits."""
  group: Group
  """Group procedure. Must be between 2 and 23."""

  model_config = ConfigDict(from_attributes=True)
