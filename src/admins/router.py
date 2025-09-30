from fastapi import APIRouter
from books.services import test_redis

admin_router = APIRouter(prefix="/api/v1/admin")


@admin_router.get("/test_redis", summary="Test redis connection", tags=["⚡Admin"])
async def tesing_redis():
    return await test_redis()