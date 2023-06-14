from fastapi import APIRouter
from src.microblog import blog
from src.user.base_config import auth_backend, fastapi_users
from src.user.schemas import UserRead, UserCreate

routes = APIRouter()

routes.include_router(
    blog.router,
    prefix="/blog"
)


# for "/login" in "/logout"
routes.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

# for "/register"
routes.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


