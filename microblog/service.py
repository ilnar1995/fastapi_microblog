from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .models import Post
from .schemas import PostCreate
from sqlalchemy import select


def create_post(db: Session, item: PostCreate):  # для синхронной
    post = Post(**item.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post_list(db: Session):                 # для синхронной
    return db.query(Post).all()

# async def get_async_post_list(session: AsyncSession) -> Post:
#     result = await session.execute(select(Post))
#     return result.scalars().all()
#
# def create_post_async(session: AsyncSession, item: PostCreate):
#     new_post = Post(**item.dict())
#     session.add(new_post)
#     return new_post