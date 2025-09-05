from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.data import get_factory
from api.error_handlers import value_error_handler
from api.routes import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
  """Application lifespan events.

  Initialize the service factory.
  """
  get_factory()
  yield


app = FastAPI(
  title="SOAT Traffic Extractor - API",
  description="API for SOAT Traffic Extractor",
  lifespan=lifespan,
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

app.add_exception_handler(ValueError, value_error_handler)  # type: ignore
