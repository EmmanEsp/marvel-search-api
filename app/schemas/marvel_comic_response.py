from pydantic import BaseModel


class MarvelComicResponse(BaseModel):

    id: int
    title: str
    image: str
    on_sale_date: str
