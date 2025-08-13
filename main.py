from pathlib import Path

from app.factories import ServiceFactory


def main():
  """Main function to run the SOAT 2025 data extraction application."""
  print("Aplicación Tarifario SOAT 2025")

  factory = ServiceFactory()

  print("Cargando capítulo 3 del tarifario SOAT 2025...")
  factory.procedure.load_data()
  print(f"{len(factory.procedure.data)} registros cargados.")

  while True:
    choice = input(
      "Seleccione una opción:\n"
      "1. Exportar procedimientos a CSV\n"
      "2. Exportar procedimientos a JSON\n"
      "0. Salir\n"
      "Opción: "
    )

    if choice == "1":
      factory.procedure.export_to_csv(Path("output/procedures.csv"))
    elif choice == "2":
      factory.procedure.export_to_json(Path("output/procedures.json"))
    elif choice == "0":
      break
    else:
      print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
  main()
