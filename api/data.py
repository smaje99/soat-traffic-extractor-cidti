from app.factories import ServiceFactory


__all__ = ("get_factory",)


__factory = None
"""Unique ServiceFactory instance for creating services in the API."""

def get_factory() -> ServiceFactory:
  """Get the unique ServiceFactory instance."""
  global __factory  # noqa: PLW0603
  if __factory is None:
      __factory = ServiceFactory()
  return __factory
