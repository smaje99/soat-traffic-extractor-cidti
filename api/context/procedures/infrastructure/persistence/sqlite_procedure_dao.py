from sqlite3 import Connection

from api.context.procedures.domain.objects import Code
from api.context.shared.infrastructure.persistence import SQLiteDAO


__all__ = ("SQLiteProcedureDAO",)


class SQLiteProcedureDAO(SQLiteDAO[Code]):
    """SQLite DAO implementation for Procedure entities."""

    def __init__(self, connection: Connection) -> None:
      """Initialize the SQLiteProcedureDAO with the appropriate table name and ID field."""
      super().__init__(connection=connection, table_name="procedures", id_field="code")
