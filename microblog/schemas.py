from pydantic import BaseModel, validator
from datetime import datetime


class PostBase(BaseModel):
    title: str
    text: str
    date: datetime

    class Config:
        orm_mode = True

    # @validator("date", pre=True)
    # def dt_validate(cls, date):
    #     print('ddddddddddddddddddddd', datetime.fromtimestamp(date))
    #     return datetime.fromtimestamp(date)

class PostList(PostBase):
    id: int

class PostCreate(PostBase):
    pass


