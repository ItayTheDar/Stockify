from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    sub: str = None
    exp: int = None
