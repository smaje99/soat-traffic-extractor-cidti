from pathlib import Path
from typing import Final, cast

from app.factories import ServiceFactory
from app.interfaces import ExportDataInterface, SQLiteExportInterface
from app.services.service import ServiceABC


MIN_CODE_PROCEDURE_LENGTH: Final = 4
MAX_CODE_PROCEDURE_LENGTH: Final = 5
MIN_CODE_GROUP_LENGTH: Final = 1
MAX_CODE_GROUP_LENGTH: Final = 2
SOAT_NOTE_AND_RESTRICTIONS: Final = """
NOTA: El costo total es una tarifa sugerida.
Esta depende de que halla hecho el procedimiento.
El cual debe estar justificado y firmando por el profesional que lo realizó.
Los valores en cero (0) tienen restricciones para ese grupo quirúrgico.
"""


def main():  # noqa: PLR0912
  """Main function to run the SOAT 2025 data extraction application."""
  print("Aplicación Tarifario SOAT 2025")

  print("Cargando tarifario SOAT 2025...")
  factory = ServiceFactory()
  exporters: list[ExportDataInterface] = [
    factory.anesthesiologist,
    factory.surgeon,
    factory.procedure,
    factory.assistant,
    factory.material,
    factory.operating_room,
    factory.pre_consultation,
    factory.cost_aggregator,
  ]
  print("Tarifario cargado correctamente.")

  while True:
    choice = input(
      "Seleccione una opción:\n"
      "1. Buscar procedimiento por código\n"
      "2. Buscar grupo quirúrgico\n"
      "3. Ver todos los grupos quirúrgicos\n"
      "4. Exportar registro a un archivo CSV\n"
      "5. Exportar registro a un archivo JSON\n"
      "6. Exportar registro a una base de datos SQLite\n"
      "0. Salir\n"
      "Opción: "
    )

    if choice == "1":
      code = input("Ingrese el código del procedimiento: ").strip()
      if not (MIN_CODE_PROCEDURE_LENGTH <= len(code) <= MAX_CODE_PROCEDURE_LENGTH):
        print(
          f"El código debe tener entre {MIN_CODE_PROCEDURE_LENGTH} y {MAX_CODE_PROCEDURE_LENGTH} caracteres."
        )
        continue

      procedure = factory.procedure.find_by_code(int(code))
      if procedure.empty:
        print("No se encontró ningún procedimiento con ese código.")
        continue

      print(f"Procedimiento encontrado:\n{procedure}\n")
      print("Información del grupo quirúrgico:")
      group = factory.cost_aggregator.find_by_group(procedure["group"].iloc[0])
      if group.empty:
        print("No se encontró información del grupo quirúrgico.")
        continue

      print(f"Grupo quirúrgico encontrado:\n{group}\n")
      print(f"Costo total del grupo quirúrgico: $ {group['total'].iloc[0]:,.0f} COP\n")
      print(SOAT_NOTE_AND_RESTRICTIONS)
    elif choice == "2":
      group_code = input("Ingrese el código del grupo quirúrgico: ").strip()
      if not (MIN_CODE_GROUP_LENGTH <= len(group_code) <= MAX_CODE_GROUP_LENGTH):
        print(
          f"El código debe tener entre {MIN_CODE_GROUP_LENGTH} y {MAX_CODE_GROUP_LENGTH} caracteres."
        )
        continue

      group = factory.cost_aggregator.find_by_group(int(group_code))
      if group.empty:
        print("No se encontró ningún grupo quirúrgico con ese código.")
        continue

      print(f"Grupo quirúrgico encontrado:\n{group}\n")
      print(f"Costo total del grupo quirúrgico: $ {group['total'].iloc[0]:,.0f} COP\n")
      print(SOAT_NOTE_AND_RESTRICTIONS)
    elif choice == "3":
      print(f"Grupos quirúrgicos disponibles:\n{factory.cost_aggregator.data}\n")
      print(SOAT_NOTE_AND_RESTRICTIONS)
    elif choice == "4":
      print("Exportando registros a CSV...")
      for exporter in exporters:
        filename = cast(ServiceABC, exporter).column
        exporter.export_to_csv(Path(f"output/{filename}.csv"))
      print("Registros exportados a CSV correctamente.")
    elif choice == "5":
      print("Exportando registros a JSON...")
      for exporter in exporters:
        filename = cast(ServiceABC, exporter).column
        exporter.export_to_json(Path(f"output/{filename}.json"))
      print("Registros exportados a JSON correctamente.")
    elif choice == "6":
      print("Exportando registros a SQLite...")
      for exporter in exporters:
        if isinstance(exporter, SQLiteExportInterface):
          exporter.export_to_sqlite()
      print("Registros exportados a SQLite correctamente.")
    elif choice == "0":
      break
    else:
      print("Opción no válida. Intente nuevamente.")

    print()


if __name__ == "__main__":
  main()
