from pydantic import BaseModel, ConfigDict

from api.context.surgical_groups.domain.objects import Group


class SurgicalGroup(BaseModel):
  """Surgical Group entity."""

  group: Group
  special: bool
  surgeon: float
  anesthesiology: float
  assistant: float
  operating_room: float
  materials: float
  presurgical: float
  preanesthetic: float
  total: float

  model_config = ConfigDict(from_attributes=True)
