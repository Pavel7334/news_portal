from fastapi import Depends, HTTPException, status
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session

from src.news.auth.database import get_async_session
from src.news.auth.schemas import NewsSchemaCreate, NewsSchemaUpdate
from src.news.models import models

from src.news.models.models import News


class NewsService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def _get_news(self, news_id: int) -> models.News:
        query = select(News).where(News.id == news_id)
        result = await self.session.execute(query)
        if not result.scalar():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result.scalar()

    async def get_list(self) -> list[News]:
        query = select(News)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_news(self, news_id: int) -> models.News:
        return await self._get_news(news_id)

    async def create(self, news_data: NewsSchemaCreate) -> models.News:
        query = insert(models.News).values(**news_data.dict()).returning(News)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.fetchone()[0]

    async def update(self, news_id: int, news_data: NewsSchemaUpdate) -> models.News:
        query = await self._get_news(news_id)
        for field, value in news_data:
            setattr(query, field, value)
        await self.session.commit()
        return query

    # async def delete(self, news_id: int):
    #     stmt = await self._get_news(news_id)
    #     await self.session.delete(stmt)
    #     await self.session.commit()

    async def delete(self, news_id: int):
        query = delete(News).where(News.id == news_id).returning(News)
        result = await self.session.execute(query)
        await self.session.commit()
        if not result.scalar():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
