from pydantic import BaseModel, HttpUrl


class ShortURLBase(BaseModel):
    url: str
    path: str


class ShortURLCreate(BaseModel):
    url: HttpUrl


class ShortURL(ShortURLBase):
    id: int

    class Config:
        orm_mode = True

