from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stie.api.endpoints import ai, analytics, auth, health, network, reports, stix
from stie.api.middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    RequestIDMiddleware,
)
from stie.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)

    app.include_router(health.router, prefix=settings.app_api_prefix, tags=["health"])
    app.include_router(auth.router, prefix=settings.app_api_prefix, tags=["auth"])
    app.include_router(reports.router, prefix=settings.app_api_prefix, tags=["reports"])
    app.include_router(network.router, prefix=settings.app_api_prefix, tags=["network"])
    app.include_router(analytics.router, prefix=settings.app_api_prefix, tags=["analytics"])
    app.include_router(ai.router, prefix=settings.app_api_prefix, tags=["ai"])
    app.include_router(stix.router, prefix=settings.app_api_prefix, tags=["stix"])

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    from stie.storage.database import close_db, init_db
    from stie.storage.qdrant_client import close_qdrant, init_qdrant
    from stie.storage.redis_client import close_redis, init_redis

    await init_db()
    await init_redis()
    await init_qdrant()

    yield

    await close_db()
    await close_redis()
    await close_qdrant()
