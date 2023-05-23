from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from . import service
from .schemas import PostCreate, PostList
from sqlalchemy.exc import IntegrityError
from .exceptions import DuplicatedEntryError

router = APIRouter()


# @router.get('/', response_model=List[PostList])
# def post_list(db: Session = Depends(get_db)):
#     return service.get_post_list(db)

@router.get('/', response_model=List[PostList])
async def post_list(db: Session = Depends(get_db)):
    return await service.get_async_post_list(db)

# @router.post('/')
# def post_list(item: PostCreate, db: Session = Depends(get_db)):
#     return service.create_post(db, item)

@router.post('/')
async def post_list(item: PostCreate, db: Session = Depends(get_db)):
    post = service.create_post_async(db, item)
    try:
        await db.commit()
        return post
    except IntegrityError as ex:
        await db.rollback()
        raise DuplicatedEntryError("The post is already stored")


