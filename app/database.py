import sqlite3


__all__ = ("get_database",)


def get_database():
  """Get a connection to the SQLite database."""
  with sqlite3.connect("database.db") as conn:
    return conn
