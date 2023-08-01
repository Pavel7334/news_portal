from fastapi import APIRouter, Depends, Response, status
from ..services.news import NewsService
from src.news.auth.schemas import NewsSchema, NewsSchemaCreate, NewsSchemaUpdate


router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get('/', response_model=list[NewsSchema])
async def get_list_news(service: NewsService = Depends()):
    return await service.get_list()


@router.get('/{news_id}', response_model=NewsSchema)
async def get_news(
    news_id: int,
    service: NewsService = Depends(),
):
    return await service.get_news(news_id)


@router.post('/', response_model=NewsSchema)
async def add_news(
    operation_data: NewsSchemaCreate,
    service: NewsService = Depends(),
):
    return await service.create(operation_data)


@router.put('/{news_id}', response_model=NewsSchema)
async def update_news(
    news_id: int,
    operation_data: NewsSchemaUpdate,
    service: NewsService = Depends()
):
    return await service.update(
        news_id,
        operation_data
    )


@router.delete('/{news_id}')
async def delete_news(
    news_id: int,
    service: NewsService = Depends(),
):
    await service.delete(news_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


