from fastapi import APIRouter

from api.context.procedures.infrastructure.http import procedure_router
from api.context.surgical_groups.infrastructure.http import surgical_group_router


__all__ = ("api_router",)


api_router = APIRouter(prefix="/api")

api_router.include_router(procedure_router, prefix="/procedures", tags=["Procedures"])
api_router.include_router(surgical_group_router, prefix="/surgical-groups", tags=["Surgical Groups"])
