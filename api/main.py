from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.data import get_factory


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
