from __future__ import annotations

from typing import Any

import httpx


class TrinoClient:
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.base_url = f"http://{host}:{port}"

    async def query(self, sql: str) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.post("/v1/statement", data=sql)
            response.raise_for_status()
            data = response.json()
            return self._parse_results(data)

    def _parse_results(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        columns = [col["name"] for col in data.get("columns", [])]
        rows = data.get("data", [])
        return [dict(zip(columns, row)) for row in rows]


trino_client = TrinoClient()
