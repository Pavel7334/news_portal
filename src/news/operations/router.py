from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.operations import NewsService
from sqlalchemy.orm import Session

from src.news.auth import schemas
from src.news.auth.database import get_async_session
from src.news.auth.schemas import NewsSchema, NewsSchemaCreate
from src.news.operations.models import News

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


# @router.get("/", response_model=List[News])  ### Для получения одной новости
# async def get_news(news_id: int, session: AsyncSession = Depends(get_async_session)):
#     query = select(news).where(news.c.id == news_id)
#     result = await session.execute(query)
#     return result.all()


@router.get('/', response_model=list[NewsSchema])
async def get_list_news(service: NewsService = Depends()):
    return await service.get_list()


@router.get('/{news_id}', response_model=NewsSchema)
async def get_news(
    news_id: int,
    service: NewsService = Depends(),
):
    return service.get_news(news_id)


@router.post('/', response_model=NewsSchema)
async def add_news(
    operation_data: NewsSchemaCreate,
    service: NewsService = Depends(),
):
    return await service.create(operation_data)


# @router.post('/')
# async def add_news(new_news: NewsSchema, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(News).values(**new_news.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}


# @router.delete("/delete/{news_id}", response_model=News)
# async def delete_news(news_id: int, News):
#     if News['id'] == News:
#         News.update(dict())
#         return {'Сообщение': f'Новость {news_id} была удалена'}
