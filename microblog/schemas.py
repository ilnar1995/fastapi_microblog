from pydantic import BaseModel, validator
from datetime import datetime
from pydantic.datetime_parse import parse_datetime


class PostBase(BaseModel):
    title: str
    text: str

class PostList(PostBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

    @validator("date", pre=True)
    def dt_validate(cls, date):
        date = parse_datetime(date)
        date = date.replace(tzinfo=None)
        return date



class PostCreate(PostBase):
    pass


