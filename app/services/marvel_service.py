import urllib.parse

from fastapi import HTTPException, status

from app.infraestructure import marvel_request
from app.schemas.marvel_character_response import MarvelCharacterResponse
from app.schemas.marvel_comic_response import MarvelComicResponse
from app.schemas.marvel_search_query_params import MarvelSearchQueryParams
from app.schemas.validate_comic_response import ValidateComicResponse
from app.settings.marvel_settings import MarvelSettings

_character_resource = "characters"
_comic_resource = "comics"


def get_character_response(results):
    characters = []
    for char in results:
        thumbnail = char["thumbnail"]
        comics = char["comics"]
        characters.append(
            MarvelCharacterResponse(
                id=char["id"],
                name=char["name"],
                image=f"{thumbnail['path']}.{thumbnail['extension']}",
                appearances=comics["available"],
            )
        )
    return characters


def get_pagination(query_params: MarvelSearchQueryParams):
    return f"limit={query_params.limit}&offset={query_params.offset}"


def get_marvel_data_by_character(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    """
    Search marvel data by character name
    """
    url_character = urllib.parse.quote(query_params.character)

    query = f"name={url_character}&"
    query = f"{_character_resource}?{query}{get_pagination(query_params=query_params)}"

    response = marvel_request.send(
        query_request=query,
        marvel_settings=marvel_settings,
    )
    results = response["data"]["results"]
    return get_character_response(results=results)


def get_comic_response(results):
    comics = []

    for comic in results:
        thumbnail = comic["thumbnail"]
        dates = comic["dates"][0]["date"]
        comics.append(
            MarvelComicResponse(
                id=comic["id"],
                title=comic["title"],
                image=f"{thumbnail['path']}.{thumbnail['extension']}",
                on_sale_date=dates,
            )
        )
    return comics


def get_marvel_data_by_comic(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    """
    Search marvel data by comic title
    """
    url_comic = urllib.parse.quote(query_params.comic)

    query = f"title={url_comic}&"
    query = f"{_comic_resource}?{query}{get_pagination(query_params=query_params)}"

    response = marvel_request.send(
        query_request=query,
        marvel_settings=marvel_settings,
    )
    results = response["data"]["results"]

    return get_comic_response(results)


def get_marvel_data_by_keyword(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    url_keyword = urllib.parse.quote(query_params.keyword)

    query_character = f"name={url_keyword}&"
    query_comic = f"title={url_keyword}&"

    query_character = f"{_character_resource}?{query_character}{get_pagination(query_params=query_params)}"
    query_comic = f"{_comic_resource}?{query_comic}{get_pagination(query_params=query_params)}"

    character_response = marvel_request.send(
        query_request=query_character,
        marvel_settings=marvel_settings,
    )
    comic_response = marvel_request.send(
        query_request=query_comic,
        marvel_settings=marvel_settings,
    )
    character_results = character_response["data"]["results"]
    comic_results = comic_response["data"]["results"]
    results = {
        "characters": get_character_response(character_results),
        "comics": get_comic_response(comic_results),
    }
    return results


def get_marvel_data_by_start_letter(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    """
    Search marvel character by initial name letter A - Z
    """
    query = f"{_character_resource}?"
    query += f"nameStartsWith={query_params.name_starts_with}&"
    query += f"limit={query_params.limit}&offset={query_params.offset}"

    response = marvel_request.send(
        query_request=query,
        marvel_settings=marvel_settings,
    )
    results = response["data"]["results"]
    return get_character_response(results)


def get_data_provider(query_params: MarvelSearchQueryParams):
    """
    Decide which filter to apply base on the priority:
    - Search by keyword into characters and comics
    - Search by name starts with A - Z
    - Search by character or comic specific name / title
    """
    if query_params.keyword:
        return get_marvel_data_by_keyword
    elif query_params.name_starts_with:
        return get_marvel_data_by_start_letter
    elif query_params.character:
        return get_marvel_data_by_character
    elif query_params.comic:
        return get_marvel_data_by_comic
    raise HTTPException(status_code=400, detail="Enter a valid filter to query")


def get_marvel_data(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    data_provider = get_data_provider(query_params=query_params)
    result = data_provider(
        query_params=query_params,
        marvel_settings=marvel_settings,
    )
    return result


def validate_comic(comic_id: int, marvel_settings: MarvelSettings):
    query = f"{_comic_resource}/{comic_id}"
    response = marvel_request.send(
        query_request=query,
        marvel_settings=marvel_settings,
    )
    if response["code"] != status.HTTP_200_OK:
        return ValidateComicResponse(isValid=False)
    return ValidateComicResponse(isValid=True)
