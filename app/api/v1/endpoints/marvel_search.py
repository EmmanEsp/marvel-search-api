from fastapi import APIRouter, Depends

from app.schemas.marvel_search_query_params import MarvelSearchQueryParams
from app.services.marvel_service import get_marvel_data
from app.settings.marvel_settings import MarvelSettings, get_marvel_settings

router = APIRouter()


@router.get("/searchComics")
def search_comics(
    *,
    query_params: MarvelSearchQueryParams = Depends(),
    marvel_settings: MarvelSettings = Depends(get_marvel_settings),
):
    return get_marvel_data(
        query_params=query_params,
        marvel_settings=marvel_settings,
    )
