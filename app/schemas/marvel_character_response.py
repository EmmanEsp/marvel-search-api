from pydantic import BaseModel


class MarvelCharacterResponse(BaseModel):

    id: int
    name: str
    image: str
    appearances: int
