from  fastapi import APIRouter
from microblog import blog
from user.base_config import auth_backend, fastapi_users
from user.schemas import UserRead, UserCreate

routes = APIRouter()

routes.include_router(blog.router, prefix="/blog")



routes.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

routes.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
