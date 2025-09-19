from typing import override

from api.context.procedures.domain import ProcedureRepository
from api.context.procedures.domain.objects import Code
from api.context.procedures.domain.procedure import Procedure

from .sqlite_procedure_dao import SQLiteProcedureDAO


__all__ = ("SQLiteProcedureRepository",)


class SQLiteProcedureRepository(ProcedureRepository):
  """SQLite implementation of the ProcedureRepository."""

  def __init__(self, dao: SQLiteProcedureDAO):
    """Initialize the repository with a SQLiteProcedureDAO instance."""
    self.__dao = dao

  @override
  def contains(self, code: Code) -> bool:
    return self.__dao.exists(code)

  @override
  def find(self, code: Code) -> Procedure | None:
    procedure_record = self.__dao.search(code)
    if procedure_record is None:
      return None

    return Procedure.model_validate(procedure_record)
