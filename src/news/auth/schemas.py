from typing import Optional, List

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class NewsSchemaBase(BaseModel):
    title: str
    description: str
    user_id: int


class NewsSchema(NewsSchemaBase):
    pass

    class Config:
        from_attributes = True


class NewsSchemaCreate(NewsSchemaBase):
    pass


class NewsSchemaUpdate(NewsSchemaBase):
    pass


class CommentSchema(BaseModel):
    id: int
    text: str
    news_id: int


class ParentCommentSchema(BaseModel):
    id: int
    text: str
    comment_id: int

    children: List[CommentSchema] = []




