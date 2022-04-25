from pydantic import BaseModel


class ValidateComicResponse(BaseModel):

    isValid: bool
