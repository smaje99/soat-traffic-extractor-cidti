from abc import ABCMeta, abstractmethod

from api.context.procedures.domain.objects import Code
from api.context.procedures.domain.procedure import Procedure


class ProcedureRepository(metaclass=ABCMeta):
  """Abstract base class for Procedure repositories."""

  @abstractmethod
  def contains(self, code: Code) -> bool:
    """Check if a procedure with the given code exists in the repository."""
    ...

  @abstractmethod
  def find(self, code: Code) -> Procedure | None:
    """Find and return a procedure by its code."""
    ...
