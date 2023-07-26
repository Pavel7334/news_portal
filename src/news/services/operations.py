from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.news.auth.database import get_async_session
from src.news.auth.schemas import NewsSchema

from src.news.operations.models import News


class NewsService:

    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    async def get_list(self) -> list[News]:
        query = select(News)
        result = await self.session.execute(query)
        return result.scalars().all()
