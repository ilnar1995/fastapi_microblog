from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Session, selectinload, joinedload
from src.core.db import Base
from sqlalchemy.exc import IntegrityError, NoResultFound
from .exceptions import DuplicatedEntryError
from src.microblog.schemas import PostCreate, PostWithId
from src.user.models import User
from sqlalchemy import select, delete, update, insert


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
            # result = await session.get(cls, id)
            query = select(cls).where(cls.id == id).options(joinedload(cls.user)) # или надо posts.c.id == id если работаем через таблицу
            result = (await session.execute(query)).scalar_one()
            return result
        except NoResultFound:
            return None

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls).order_by(cls.id)  # .options(selectinload(cls.user)) для стягивания модели user при загрузке
        return (await session.execute(query)).scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, item: PostCreate):
        new_post = cls(**item.dict())
        session.add(new_post)       # добавление объекта в сеанс
        # stmt = insert(cls).values(**item.dict()).returning(cls)
        # new_post = await session.execute(stmt)
        try:
            await session.commit()  # чтоб транзакция завершилась
            await session.refresh(new_post)
            return new_post
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError("The post is already stored")

    @classmethod
    async def update(cls, session: AsyncSession, item: PostCreate, id: int):
        stmt = update(cls).where(cls.id == id).values(**item.dict()).returning(cls)
        result = await session.execute(stmt)
        try:
            await session.commit()
            return result.first()[0]
        except IntegrityError as ex:
            await session.rollback()
            raise DuplicatedEntryError("Error")

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        query = select(cls).where(cls.id == id)
        post = await session.execute(query)
        try:
            post = post.scalar_one()
            await session.delete(post)
            await session.commit()
        except:
            raise DuplicatedEntryError("The post is not founed")
        # stmt = delete(cls, id).where(cls.id == id)
        # await session.delete(stmt)
        # try:
        #     await session.commit()
        # except:
        #     return False
        return True

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

posts = Post.__table__
