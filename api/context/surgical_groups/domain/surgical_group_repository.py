from abc import ABCMeta, abstractmethod

from api.context.procedures.domain.objects import Code
from api.context.surgical_groups.domain.surgical_group import SurgicalGroup


class SurgicalGroupRepository(metaclass=ABCMeta):
  """Abstract base class for SurgicalGroup repositories."""

  @abstractmethod
  def contains(self, code: Code) -> bool:
    """Check if a surgical group with the given code exists in the repository."""
    ...

  @abstractmethod
  def find(self, code: Code) -> SurgicalGroup | None:
    """Find and return a surgical group by its code."""
    ...
