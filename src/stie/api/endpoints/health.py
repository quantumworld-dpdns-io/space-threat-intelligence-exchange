from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from stie.storage.database import get_session
from stie.storage.redis_client import get_redis
from stie.config.settings import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = "error"

    return {"status": db_status, "type": "postgresql"}


@router.get("/health/redis")
async def redis_health():
    redis_client = await get_redis()
    try:
        await redis_client.ping()
        redis_status = "ok"
    except Exception as e:
        redis_status = "error"

    return {"status": redis_status, "type": "redis"}
