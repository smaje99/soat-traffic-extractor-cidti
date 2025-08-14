from pathlib import Path
from typing import Final

from app.factories import ServiceFactory


MIN_CODE_PROCEDURE_LENGTH: Final = 4
MAX_CODE_PROCEDURE_LENGTH: Final = 5


def main():
  """Main function to run the SOAT 2025 data extraction application."""
  print("Aplicación Tarifario SOAT 2025")

  factory = ServiceFactory()

  print("Cargando tarifario SOAT 2025...")
  factory.procedure.load_data()
  print(f"{len(factory.procedure.data)} registros cargados...")
  factory.surgical_professional.load_data()
  print(f"{len(factory.surgical_professional.data)} registros cargados.")

  while True:
    choice = input(
      "Seleccione una opción:\n"
      "1. Exportar procedimientos a CSV\n"
      "2. Exportar procedimientos a JSON\n"
      "3. Buscar procedimiento por código\n"
      "4. Buscar procedimientos por grupo quirúrgico\n"
      "5. Buscar cuotas de profesional quirúrgico por grupo quirúrgico\n"
      "0. Salir\n"
      "Opción: "
    )

    if choice == "1":
      factory.procedure.export_to_csv(Path("output/procedures.csv"))
    elif choice == "2":
      factory.procedure.export_to_json(Path("output/procedures.json"))
    elif choice == "3":
      code = input(
        "Ingrese el código del procedimiento (entre "
        f"{MIN_CODE_PROCEDURE_LENGTH} y {MAX_CODE_PROCEDURE_LENGTH} dígitos): "
      )
      if len(code) < MIN_CODE_PROCEDURE_LENGTH or len(code) > MAX_CODE_PROCEDURE_LENGTH:
        print("Código inválido. Debe tener entre 4 y 5 dígitos.")
        continue

      result = factory.procedure.find_by_code(int(code))
      if result.empty:
        print("Procedimiento no encontrado.")
        continue

      print("Procedimiento encontrado:")
      print(result)
    elif choice == "4":
      group = input("Ingrese el grupo del procedimiento: ")
      result = factory.procedure.find_by_group(int(group))
      if result.empty:
        print("Procedimientos no encontrados.")
        continue

      print("Procedimientos encontrados:")
      print(result)
    elif choice == "5":
      group = input("Ingrese el grupo quirúrgico: ")
      result = factory.surgical_professional.find_by_group(int(group))
      if result.empty:
        print("Cuotas no encontradas.")
        continue

      print("Cuotas encontradas:")
      print(result)
    elif choice == "0":
      break
    else:
      print("Opción no válida. Intente nuevamente.")

    print()


if __name__ == "__main__":
  main()
