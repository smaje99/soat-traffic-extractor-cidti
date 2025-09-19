from sqlite3 import Connection

from api.context.shared.infrastructure.persistence import SQLiteDAO
from api.context.surgical_groups.domain.objects import Group


__all__ = ("SQLiteSurgicalGroupDAO",)


class SQLiteSurgicalGroupDAO(SQLiteDAO[Group]):
    """SQLite DAO implementation for Surgical Group entities."""

    def __init__(self, connection: Connection) -> None:
      """Initialize the SQLiteSurgicalGroupDAO with the appropriate table name and ID field."""
      super().__init__(connection=connection, table_name="surgical_groups", id_field="group")
