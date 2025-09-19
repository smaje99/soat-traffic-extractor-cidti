from abc import ABCMeta, abstractmethod
from typing import Any

from api.core.persistence.expression import Expression


__all__ = ("DAO",)


class DAO[EntityId](metaclass=ABCMeta):
  """Generic DAO interface."""

  @abstractmethod
  def search(self, entity_id: EntityId) -> dict[str, Any] | None:
    """Search an entity.

    Args:
        entity_id (EntityId): Entity id.

    Returns:
        dict[str, Any]: Found entity.
    """

  @abstractmethod
  def filter(self, expression: Expression) -> list[dict[str, Any]]:
    """Filter entities.

    Args:
        expression (Expression): Expression to filter.

    Returns:
        list[dict[str, Any]]: Filtered entities.
    """

  @abstractmethod
  def exists(self, entity_id: EntityId) -> bool:
    """Check if an entity exists.

    Args:
        entity_id (EntityId): Entity id.

    Returns:
        bool: True if entity exists, False otherwise.
    """
