from __future__ import annotations

from typing import Any

import httpx

from stie.config.settings import settings


class LLMClient:
    def __init__(self):
        self.provider = settings.ai_llm_provider
        self.model = settings.ai_llm_model
        self.api_url = settings.ai_llm_api_url
        self.api_key = settings.ai_llm_api_key
        self.client: httpx.AsyncClient | None = None

    async def _ensure_client(self):
        if self.client is None:
            self.client = httpx.AsyncClient(base_url=self.api_url, timeout=60.0)

    async def complete(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        await self._ensure_client()
        if self.provider == "ollama":
            return await self._ollama_complete(prompt, system_prompt, **kwargs)
        elif self.provider in ("openai", "vllm"):
            return await self._openai_complete(prompt, system_prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def _ollama_complete(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt

        response = await self.client.post("/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    async def _openai_complete(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs,
        }

        response = await self.client.post("/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self):
        if self.client:
            await self.client.aclose()


llm_client = LLMClient()
