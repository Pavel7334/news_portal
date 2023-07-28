from fastapi import Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.orm import Session, session

from src.news.auth.database import get_async_session
from src.news.auth.schemas import NewsSchema, NewsSchemaCreate
from src.news.operations import models

from src.news.operations.models import News


class NewsService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def get_list(self) -> list[News]:
        query = select(News)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_news(self, news_id: int) -> models.News:
        query = select(News).where(News.id == news_id)
        result = await self.session.execute(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result.scalar()

    async def create(self, operation_data: NewsSchemaCreate) -> models.News:
        stmt = insert(models.News).values(**operation_data.dict()).returning(News)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.fetchone()[0]
