from typing import List

from pydantic import BaseModel, validator
from datetime import datetime
from pydantic.datetime_parse import parse_datetime
from sqlalchemy.orm import Relationship

from src.user.schemas import UserRead


class PostBase(BaseModel):
    title: str
    text: str

class PostList(PostBase):
    id: int
    date: datetime
    user: UserRead = None
    class Config:
        orm_mode = True

class PostWithId(PostBase):
    id: int
    date: datetime
    class Config:
        orm_mode = True

    # @validator("date", pre=True)
    # def dt_validate(cls, date):
    #     date = parse_datetime(date)
    #     date = date.replace(tzinfo=None)
    #     return date



class PostCreate(PostBase):
    pass


