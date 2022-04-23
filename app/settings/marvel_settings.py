from functools import lru_cache

from pydantic import BaseSettings


class MarvelSettings(BaseSettings):
    """Marvel Settings
    Store all marvel config envs
    """

    marvel_private_key: str
    marvel_public_key: str
    marvel_base_url: str


@lru_cache()
def get_marvel_settings():
    return MarvelSettings()
