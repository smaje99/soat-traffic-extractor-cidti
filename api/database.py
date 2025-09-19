import sqlite3


__all__ = ("get_database_connection",)


def get_database_connection() -> sqlite3.Connection:
  """Get a connection to the SQLite database."""
  with sqlite3.connect("database.db") as conn:
    return conn
