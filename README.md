# SOAT Traffic Extractor CIDTI

## Objetivo del Proyecto

Este proyecto tiene como objetivo automatizar la extracción, procesamiento y exportación de la información contenida en el tarifario SOAT 2025, facilitando la consulta, análisis y exportación de datos relacionados con procedimientos, profesionales y costos quirúrgicos. Permite buscar procedimientos y grupos quirúrgicos, así como exportar los datos a formatos CSV y JSON de manera estructurada.

## Instalación de Dependencias

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

> Se recomienda usar [uv](https://github.com/astral-sh/uv) para este proyecto, ya que fue construido sobre este marco.

1. **Clonar el repositorio:**

   ```sh
   git clone <url-del-repositorio>
   cd soat-traffic-extractor-cidti
   ```
2. **Crear y activar un entorno virtual (opcional pero recomendado):**

   ```sh
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```
3. **Instalar dependencias:**

   ```sh
   pip install -r requirements.txt
   ```

   O usando [uv](https://github.com/astral-sh/uv):

   ```sh
   uv pip install -r requirements.txt
   ```

## Ejecución del Proyecto

Para iniciar la aplicación principal:

```sh
python main.py
```

El sistema mostrará un menú interactivo en consola para realizar búsquedas y exportaciones sobre el tarifario SOAT 2025.

## Arquitectura de Capas

El proyecto sigue una arquitectura modular y por capas, facilitando la mantenibilidad y escalabilidad:

- **Capa de Presentación:**

  - `main.py`: Punto de entrada. Gestiona la interacción con el usuario y orquesta las operaciones principales.
- **Capa de Aplicación y Servicios:**

  - `app/`: Contiene la lógica de negocio y utilidades.
    - `factories.py`: Fábricas para instanciar servicios y exportadores.
    - `interfaces.py`: Define interfaces y contratos para los servicios y exportadores.
    - `utils.py`: Funciones utilitarias generales.
    - `parser.py`: Lógica de parsing y procesamiento de texto extraído de PDFs.
    - `exporter.py`: Implementaciones para exportar datos a diferentes formatos.
    - `extractor.py`: Funciones para extracción de texto desde PDF.
    - `services/`: Servicios especializados para cada tipo de dato (procedimientos, profesionales, costos, etc.).
      - `procedure.py`, `anesthesiologist.py`, `surgeon.py`, `assistant.py`, `material.py`, `operating_room.py`, `pre_consultation.py`, `cost_aggregator.py`, `service.py`: Cada archivo implementa la lógica de negocio y acceso a datos para su dominio específico.
- **Capa de Datos:**

  - `data/`: Almacena los archivos fuente, como el PDF del tarifario SOAT 2025.
  - `output/`: Carpeta de salida para los archivos exportados (CSV, JSON).
- **Capa de Pruebas:**

  - `tests/`: Pruebas unitarias para cada servicio y componente principal. Utiliza `pytest` y fixtures para facilitar el testeo y la reutilización de código de prueba.
- **Capa de Notebooks:**

  - `notebooks/`: Notebooks de Jupyter para experimentación, pruebas de extracción y procesamiento de datos.

## Pruebas

Para ejecutar los tests unitarios:

```sh
pytest
```

## Estilo y Calidad de Código

El proyecto utiliza herramientas como `black`, `isort`, `flake8`, `mypy` y `ruff` para asegurar la calidad, el tipado y el estilo del código. Puedes ejecutar los linters con:

```sh
ruff check .
black --check .
isort --check .
flake8 .
mypy .
```

## Notas Adicionales

- El proyecto está preparado para Python 3.12 o superior.
- Se recomienda mantener el entorno virtual activo durante el desarrollo y pruebas.
- Los datos exportados se almacenan en la carpeta `output/`.
- El PDF fuente debe estar en la carpeta `data/`.

---
## Módulo API (FastAPI)

El módulo `api` implementa una API RESTful utilizando FastAPI, permitiendo exponer los servicios y datos del tarifario SOAT 2025 a través de endpoints HTTP. Esta API facilita la integración con sistemas externos, aplicaciones web y automatización de consultas y exportaciones.

### Estructura del módulo

```
api/
├── __init__.py
├── main.py              # Punto de entrada de la API (instancia FastAPI)
├── routes.py            # Definición de rutas/endpoints principales
├── daos.py              # Acceso a datos y lógica de persistencia
├── data.py              # Estructuras y utilidades para manejo de datos
├── error_handlers.py    # Gestión de errores y excepciones personalizadas
├── schemas.py           # Esquemas Pydantic para validación y serialización
└── controllers/
  ├── __init__.py
  ├── procedure.py     # Controlador para procedimientos
  └── surgical_group.py# Controlador para grupos quirúrgicos
```

### Objetivo y funcionalidades

- Exponer los datos y servicios del tarifario SOAT 2025 mediante endpoints RESTful.
- Permitir búsquedas de procedimientos y grupos quirúrgicos vía HTTP.
- Gestionar errores y respuestas consistentes.

### Ejecución de la API

Para iniciar el servidor de desarrollo de la API:

```sh
uv run fastapi dev api/main.py
```

O usando directamente FastAPI/Uvicorn:

```sh
uvicorn api.main:app --reload
```

La API estará disponible en `http://localhost:8000` por defecto.

### Endpoints principales

Algunos endpoints típicos:

- `api/procedures/{code}` — Consulta de procedimiento por código.
- `api/surgical-groups/{code}` — Consulta de grupo quirúrgico por código.

### Esquemas y validación

El módulo `schemas.py` define los modelos Pydantic para validar y serializar los datos de entrada/salida, asegurando respuestas estructuradas y seguras.

### Manejo de errores

`error_handlers.py` centraliza la gestión de errores, devolviendo respuestas HTTP claras y consistentes ante excepciones o validaciones fallidas.

### Pruebas y desarrollo

Se recomienda probar los endpoints usando herramientas como [Swagger UI](http://localhost:8000/docs) (incluida por defecto en FastAPI), [Postman](https://www.postman.com/) o curl.

---

CIDTI - Prácticas en Empresa - UNIR
