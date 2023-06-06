from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Session, selectinload
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
    date = Column(DateTime,  index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, back_populates="posts", lazy="joined")

    # __mapper_args__ = {"eager_defaults": True}

    @classmethod
    async def get(cls, session: AsyncSession, id: int):
        try:
            result = await session.get(cls, id)
            # result = await session.get(cls, id)
        except NoResultFound:
            return None
        return result

    @classmethod
    async def get_all(cls, session: AsyncSession):
        return (await session.execute(select(Post).order_by(cls.id))).scalars().all()  # .options(selectinload(cls.user)) внутри скобок метода execute для стягивания модели user при загрузке

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

    # @classmethod
    # def create_post(db: Session, item: PostCreate):  # для синхронной
    #     post = Post(**item.dict())
    #     db.add(post)
    #     db.commit()
    #     db.refresh(post)
    #     return post
    #
    # @classmethod
    # def get_post_list(db: Session):  # для синхронной
    #     return db.query(Post).all()
