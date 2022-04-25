import hashlib
import time

import requests
from fastapi import HTTPException, status

from app.settings.marvel_settings import MarvelSettings


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


def send(query_request: str, marvel_settings: MarvelSettings):
    url = f"{marvel_settings.marvel_base_url}{query_request}"
    auth_payload = _get_auth_payload(marvel_settings=marvel_settings)
    response = requests.get(
        url=url,
        params=auth_payload
    ).json()
    if response["code"] != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)
    return response
