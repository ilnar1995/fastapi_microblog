from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.core.db import get_db_session
from .schemas import PostCreate, PostList, PostBase, PostWithId
from .models import Post

router = APIRouter()


# @router.get('/', response_model=List[PostList])
# def post_list(db: Session = Depends(get_db)):
#     return service.get_post_list(db)

@router.get('/posts', response_model=List[PostList])
async def post_list(db: AsyncSession = Depends(get_db_session)):
    return await Post.get_all(db)

# @router.post('/')
# def post_list(item: PostCreate, db: Session = Depends(get_db)):
#     return service.create_post(db, item)

@router.post('/post', response_model=PostList)
async def create_post(item: PostCreate, db: AsyncSession = Depends(get_db_session)):
    posts = await Post.create(db, item)
    return posts

@router.patch('/post', response_model=PostWithId)
async def create_post(id: int, item: PostCreate, db: AsyncSession = Depends(get_db_session)):
    posts = await Post.update(db, item, id)
    return posts

@router.get("/post", response_model=PostList)
async def get_post(id: int, db: AsyncSession = Depends(get_db_session)):
    post = await Post.get(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return post

@router.delete("/post")
async def get_post(id: int, db: AsyncSession = Depends(get_db_session)):
    post = await Post.delete(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return {'status':'succsess'}
