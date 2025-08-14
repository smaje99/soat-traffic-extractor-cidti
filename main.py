from pathlib import Path
from typing import Final

from app.factories import ServiceFactory


MIN_CODE_PROCEDURE_LENGTH: Final = 4
MAX_CODE_PROCEDURE_LENGTH: Final = 5
MIN_CODE_GROUP_LENGTH: Final = 1
MAX_CODE_GROUP_LENGTH: Final = 2


def main():
  """Main function to run the SOAT 2025 data extraction application."""
  print("Aplicación Tarifario SOAT 2025")

  print("Cargando tarifario SOAT 2025...")
  factory = ServiceFactory()
  print("Tarifario cargado correctamente.")

  while True:
    choice = input(
      "Seleccione una opción:\n"
      "1. Buscar procedimiento por código\n"
      "2. Buscar grupo quirúrgico\n"
      "3. Ver todos los grupos quirúrgicos\n"
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
      print(
        "NOTA: El costo total es una tarifa sugerida.\n",
        "Esta depende de que halla hecho el procedimiento.",
        "El cual debe estar justificado y firmando por el profesional que lo realizó.\n"
      )
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
      print(
        "NOTA: El costo total es una tarifa sugerida.\n",
        "Esta depende de que halla hecho el procedimiento.",
        "El cual debe estar justificado y firmando por el profesional que lo realizó.\n"
      )
    elif choice == "3":
      print(f"Grupos quirúrgicos disponibles:\n{factory.cost_aggregator.data}\n")
      print(
        "NOTA: El costo total es una tarifa sugerida.\n",
        "Esta depende de que halla hecho el procedimiento.",
        "El cual debe estar justificado y firmando por el profesional que lo realizó.\n",
        "Los valores en cero (0) tienen restricciones para ese grupo quirúrgico.\n",
      )
    elif choice == "0":
      break
    else:
      print("Opción no válida. Intente nuevamente.")

    print()


if __name__ == "__main__":
  main()
