from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


# Shared properties
class ShortUrlBase(BaseModel):
    destination: HttpUrl
    key: Optional[str] = Field(
        None,
        min_length=1,
        max_length=25,
        regex=r'^[a-zA-Z\d-]+$',
    )


# Properties to receive on item creation
class ShortUrlCreate(ShortUrlBase):
    pass


# Properties to receive via API on update
class ShortUrlUpdate(ShortUrlBase):
    pass


# Properties to return to client
class ShortUrl(ShortUrlBase):
    id: int

    class Config:
        orm_mode = True
