from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.containers import ApplicationContainer
from api.middlewares.error_handlers import value_error_handler
from api.routes import api_router


# Initialize Dependency Injection container
container = ApplicationContainer()

app = FastAPI(
  title="SOAT Traffic Extractor - API",
  description="API for SOAT Traffic Extractor",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(api_router)

app.add_exception_handler(ValueError, value_error_handler)  # type: ignore
