from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from src.news.auth.auth import auth_backend
from src.news.auth.database import User
from src.news.auth.manager import get_user_manager
from src.news.auth.schemas import UserRead, UserCreate

from src.news.operations.router import router as router_operation

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

app.include_router(router_operation)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
