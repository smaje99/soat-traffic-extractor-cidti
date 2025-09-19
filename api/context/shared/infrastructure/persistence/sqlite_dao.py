from abc import ABCMeta
from sqlite3 import Connection
from typing import Any, override

from api.context.shared.domain.dao import DAO
from api.core.persistence.expression import Expression


__all__ = ("SQLiteDAO",)


class SQLiteDAO[EntityId](DAO[EntityId], metaclass=ABCMeta):
  """SQLite DAO implementation."""

  def __init__(self, connection: Connection, table_name: str, id_field: str = "id"):
    """Initialize the SQLiteDAO with a database connection and table name.

    Args:
        connection (Connection): The SQLite database connection.
        table_name (str): The name of the table to operate on.
        id_field (str, optional): The name of the ID field. Defaults to "id".
    """
    self.connection = connection
    self.table_name = table_name
    self.id_field = id_field

  @override
  def search(self, entity_id: EntityId) -> dict[str, Any] | None:
    query = f"SELECT * FROM {self.table_name} WHERE {self.id_field} = ?"
    cursor = self.connection.execute(query, (entity_id,))
    row = cursor.fetchone()
    if not row:
      return None
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row, strict=False))

  @override
  def filter(self, expression: Expression) -> list[dict[str, Any]]:
    query = f"SELECT * FROM {self.table_name}"
    cursor = self.connection.execute(query)
    columns = [column[0] for column in cursor.description]

    if not expression:
      return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

    where_clause, params = expression.to_sql()
    query += f" WHERE {where_clause}"
    cursor = self.connection.execute(query, params)
    return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

  @override
  def exists(self, entity_id: EntityId) -> bool:
    query = f"SELECT 1 FROM {self.table_name} WHERE {self.id_field} = ?"
    cursor = self.connection.execute(query, (entity_id,))
    return cursor.fetchone() is not None
