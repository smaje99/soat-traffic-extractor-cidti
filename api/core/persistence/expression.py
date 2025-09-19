from abc import ABCMeta, abstractmethod
from string import Template
from typing import Any, Literal, override


__all__ = (
  "Expression",
  "SimpleExpression",
  "AndExpression",
  "OrExpression",
  "NotExpression",
)


Operator = Literal["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN"]
"""Supported operators for expressions."""


class Expression(metaclass=ABCMeta):
  """Generic expression interface.

  Based on the Criteria pattern and inspired by SQLAlchemy expressions.
  """

  @abstractmethod
  def to_sql(self) -> tuple[str, list[Any]]:
    """Convert the expression to a SQL string.

    Returns:
        str: SQL string.
    """
    ...


class SimpleExpression(Expression):
  """Simple expression implementation."""

  def __init__(self, field: str, operator: Operator, value: Any):
    """Initialize a SimpleExpression with a field, operator, and value.

    Args:
        field (str): The field name to filter on.
        operator (Operator): The comparison operator.
        value (Any): The value to compare the field against.
    """
    self.field = field
    self.operator = operator
    self.value = value

  @override
  def to_sql(self) -> tuple[str, list[Any]]:
    if self.operator == "IN" and isinstance(self.value, list):
      placeholders = ", ".join(["%s"] * len(self.value))  # type: ignore
      sql_template = Template("$field $operator ($placeholders)")
      sql = sql_template.substitute(
        field=self.field, operator=self.operator, placeholders=placeholders
      )
      return sql, self.value  # type: ignore
    elif self.operator == "LIKE":
      sql_template = Template("$field $operator %s")
      sql = sql_template.substitute(field=self.field, operator=self.operator)
      return sql, [f"%{self.value}%"]
    else:
      sql_template = Template("$field $operator %s")
      sql = sql_template.substitute(field=self.field, operator=self.operator)
      return sql, [self.value]


class CompositeExpression(Expression, metaclass=ABCMeta):
  """Composite expression implementation."""

  def __init__(self, operator: Literal["AND", "OR"], *expressions: Expression):
    self.operator = operator
    self.expressions = expressions

  @override
  def to_sql(self) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    for expr in self.expressions:
      clause, values = expr.to_sql()
      clauses.append(f"({clause})")
      params.extend(values)

    return f" {self.operator} ".join(clauses), params


class AndExpression(CompositeExpression):
  """AND composite expression."""

  def __init__(self, *expressions: Expression):
    """Initialize an AndExpression with multiple expressions.

    Args:
        *expressions (Expression): Expressions to combine with AND.
    """
    super().__init__("AND", *expressions)


class OrExpression(CompositeExpression):
  """OR composite expression."""

  def __init__(self, *expressions: Expression):
    """Initialize an OrExpression with multiple expressions.

    Args:
        *expressions (Expression): Expressions to combine with OR.
    """
    super().__init__("OR", *expressions)


class NotExpression(Expression):
  """NOT expression implementation."""

  def __init__(self, expression: Expression):
    """Initialize a NotExpression with a single expression.

    Args:
        expression (Expression): The expression to negate.
    """
    self.expression = expression

  @override
  def to_sql(self) -> tuple[str, list[Any]]:
    clause, params = self.expression.to_sql()
    return f"NOT ({clause})", params
