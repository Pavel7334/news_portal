from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from starlette import status

from src.news.auth.database import get_async_session
from src.news.auth.schemas import CommentSchema
from src.news.models import models
from src.news.models.models import Comment


class CommentService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def _get_comment(self, comment_id: int) -> models.Comment:
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result.scalar()

    async def get_list(self) -> list[Comment]:
        query = select(Comment)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_comment(self, comment_id: int) -> models.Comment:
        return await self._get_comment(comment_id)

    async def create(self, comment_data: CommentSchema) -> models.Comment:
        query = insert(models.Comment).values(**comment_data.dict()).returning(Comment)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.fetchone()[0]
