from fastapi import APIRouter, Depends, Response, status

from ..services.commit import CommentService
from ..services.news import NewsService
from src.news.auth.schemas import NewsSchema, NewsSchemaCreate, NewsSchemaUpdate, CommentSchema

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
    news_data: NewsSchemaCreate,
    service: NewsService = Depends(),
):
    return await service.create(news_data)


@router.put('/{news_id}', response_model=NewsSchema)
async def update_news(
    news_id: int,
    news_data: NewsSchemaUpdate,
    service: NewsService = Depends()
):
    return await service.update(
        news_id,
        news_data
    )


@router.delete('/{news_id}')
async def delete_news(
    news_id: int,
    service: NewsService = Depends(),
):
    await service.delete(news_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/{comment_id}', response_model=CommentSchema)
async def add_comment(
    comment_data: CommentSchema,
    service: CommentService = Depends(),
):
    return await service.create(comment_data)


@router.get('{news_id}/comment', response_model=CommentSchema)
async def get_comment(
    comment_id: int,
    service: CommentService = Depends(),
):
    return await service.get_comment(comment_id)

