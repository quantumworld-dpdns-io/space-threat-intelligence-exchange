from __future__ import annotations

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
)

from stie.config.settings import settings

qdrant_client: AsyncQdrantClient | None = None


async def init_qdrant():
    global qdrant_client
    qdrant_client = AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key or None,
    )

    collections = await qdrant_client.get_collections()
    exists = any(c.name == settings.qdrant_collection for c in collections.collections)

    if not exists:
        await qdrant_client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.ai_embedding_dimension,
                distance=Distance.COSINE,
            ),
        )


async def close_qdrant():
    global qdrant_client
    if qdrant_client:
        await qdrant_client.close()
        qdrant_client = None


async def get_qdrant() -> AsyncQdrantClient:
    if qdrant_client is None:
        raise RuntimeError("Qdrant not initialized")
    return qdrant_client
