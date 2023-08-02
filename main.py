from urllib.request import Request

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from starlette import status
from starlette.responses import JSONResponse

from src.news.auth.auth import auth_backend
from src.news.auth.manager import get_user_manager
from src.news.auth.schemas import UserRead, UserCreate
from src.news.models.models import User

from src.news.models.router import router as router_news

app = FastAPI(
    title="Новостной портал"
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_news)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


@app.exception_handler(Exception)
async def base_exception_handler(request: Request, exc: Exception):
    """Exception handler for all exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': str(exc)},
    )