from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.news.auth.database import get_async_session
from src.news.auth.schemas import News
from src.news.operations.models import news

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/")
async def get_news(news_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(news).where(news.c.id == news_id)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_news(new_news: News, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(news).values(**new_news.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
