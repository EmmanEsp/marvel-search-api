from fastapi import APIRouter, status

from app.api.v1.endpoints import marvel_search

v1_api_router = APIRouter()

v1_api_router.include_router(
    marvel_search.router,
    tags=["Marvel Search"],
    prefix="/marvel-search",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
