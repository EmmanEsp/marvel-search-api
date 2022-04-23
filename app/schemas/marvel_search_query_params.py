from typing import Optional


class MarvelSearchQueryParams:

    def __init__(
        self,
        keyword: Optional[str] = None,
        name_starts_with: Optional[str] = None,
        character: Optional[str] = None,
        comic: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ):
        self.character = character
        self.comic = comic
        self.name_starts_with = name_starts_with
        self.keyword = keyword
        self.offset = offset
        self.limit = limit
