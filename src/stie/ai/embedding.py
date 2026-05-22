from __future__ import annotations

import httpx
import numpy as np

from stie.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.model = settings.ai_embedding_model
        self.dimension = settings.ai_embedding_dimension
        self.api_url = settings.ai_llm_api_url
        self.provider = settings.ai_llm_provider

    async def generate_embedding(self, text: str) -> list[float]:
        if self.provider == "ollama":
            return await self._ollama_embed(text)
        elif self.provider in ("openai", "vllm"):
            return await self._openai_embed(text)
        return np.zeros(self.dimension).tolist()

    async def _ollama_embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient(base_url=self.api_url, timeout=30.0) as client:
            response = await client.post("/api/embeddings", json={
                "model": self.model,
                "prompt": text,
            })
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])

    async def _openai_embed(self, text: str) -> list[float]:
        headers = {"Content-Type": "application/json"}
        if settings.ai_llm_api_key:
            headers["Authorization"] = f"Bearer {settings.ai_llm_api_key}"

        async with httpx.AsyncClient(base_url=self.api_url, timeout=30.0) as client:
            response = await client.post("/v1/embeddings", json={
                "model": self.model,
                "input": text,
            }, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            emb = await self.generate_embedding(text)
            embeddings.append(emb)
        return embeddings


embedding_service = EmbeddingService()
