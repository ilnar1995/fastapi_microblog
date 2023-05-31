from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from core.db import Base
from sqlalchemy.exc import IntegrityError, NoResultFound
from .exceptions import DuplicatedEntryError
from microblog.schemas import PostCreate
from user.models import User
from sqlalchemy import select


class Post(Base):
    __tablename__ = "microblog_posts"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    text = Column(String(350))
    date = Column(DateTime)
    user = Column(Integer, ForeignKey("user.id"))
    user_id = relationship(User)

    @classmethod
    async def get(cls, session: AsyncSession, id: int):
        try:
            result = await session.get(cls, id)
        except NoResultFound:
            return None
        return result

    @classmethod
    async def get_all(cls, session: AsyncSession):
        result = await session.execute(select(Post))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, item: PostCreate):
        new_post = cls(**item.dict())
        session.add(new_post)
        try:
            await session.commit()
            await session.refresh(new_post)
            return new_post
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError("The post is already stored")
        return new_post
