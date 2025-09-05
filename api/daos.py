from typing import Any

from pandas import DataFrame


__all__ = ("get_procedure_dao", "get_surgical_group_dao")


def get_procedure_dao(dataframe: DataFrame) -> dict[str, Any]:
  """Get procedure DAO from dataframe."""
  return {
    "code": dataframe["code"].iloc[0],
    "group": dataframe["group"].iloc[0],
  }


def get_surgical_group_dao(dataframe: DataFrame) -> dict[str, Any]:
  """Get surgical group DAO from dataframe."""
  return {
    "group": dataframe["group"].iloc[0],
    "special": dataframe["special"].iloc[0],
    "surgeon": dataframe["cirujano"].iloc[0],
    "anesthesiology": dataframe["anestesiología"].iloc[0],
    "assistant": dataframe["ayudantía"].iloc[0],
    "operating_room": dataframe["sala de cirugía"].iloc[0],
    "materials": dataframe["instrumentario"].iloc[0],
    "presurgical": dataframe["prequirúrgica"].iloc[0],
    "preanesthetic": dataframe["preanestésica"].iloc[0],
    "total": dataframe["total"].iloc[0],
  }
