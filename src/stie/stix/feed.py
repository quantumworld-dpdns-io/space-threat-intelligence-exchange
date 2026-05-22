from __future__ import annotations

from typing import Any

import httpx


class TAXIIClient:
    def __init__(self, server_url: str, collection_id: str = "default"):
        self.server_url = server_url.rstrip("/")
        self.collection_id = collection_id
        self.client = httpx.AsyncClient(timeout=30.0)

    async def poll_objects(self, added_after: str | None = None) -> list[dict[str, Any]]:
        url = f"{self.server_url}/collections/{self.collection_id}/objects"
        params = {}
        if added_after:
            params["added_after"] = added_after
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("objects", [])

    async def get_collections(self) -> list[dict[str, Any]]:
        response = await self.client.get(f"{self.server_url}/collections")
        response.raise_for_status()
        data = response.json()
        return data.get("collections", [])

    async def close(self):
        await self.client.aclose()


async def fetch_external_feeds(feed_urls: list[str]) -> list[dict[str, Any]]:
    all_reports = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for url in feed_urls:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                objects = data.get("objects", []) if isinstance(data, dict) else data
                all_reports.extend(objects)
            except Exception:
                pass
    return all_reports
