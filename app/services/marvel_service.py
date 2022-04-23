import hashlib
import time

import requests

from app.schemas.marvel_search_query_params import MarvelSearchQueryParams
from app.settings.marvel_settings import MarvelSettings

_character_resource = "characters"
_comic_resource = "comics"


def _get_auth_payload(marvel_settings: MarvelSettings):
    timestamp = time.time()
    hash_str = f"{timestamp}{marvel_settings.marvel_private_key}{marvel_settings.marvel_public_key}"
    hash_digest = hashlib.md5(hash_str.encode()).hexdigest()
    payload = {
        "apikey": marvel_settings.marvel_public_key,
        "ts": f"{timestamp}",
        "hash": f"{hash_digest}"
    }
    return payload


def _send_request(query_request: str, marvel_settings: MarvelSettings):
    url = f"{marvel_settings.marvel_base_url}{query_request}"
    auth_payload = _get_auth_payload(marvel_settings=marvel_settings)
    result = requests.get(
        url=url,
        params=auth_payload
    )
    return result.json()


def get_marvel_data(query_params: MarvelSearchQueryParams, marvel_settings: MarvelSettings):
    query = f"{_character_resource}?"
    query += f"limit={query_params.limit}&offset={query_params.offset}"
    result = _send_request(
        query_request=query,
        marvel_settings=marvel_settings,
    )
    return result
