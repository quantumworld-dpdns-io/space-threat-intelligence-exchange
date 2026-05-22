from __future__ import annotations

from typing import Any

from stie.ai.client import llm_client

RAG_SYSTEM_PROMPT = """You are a space threat intelligence assistant. Answer questions based on the provided threat report context.
If the context does not contain enough information, say so clearly.
Cite specific report IDs when referencing information."""


async def answer_question(question: str, context_reports: list[dict[str, Any]]) -> str:
    context_text = "\n\n".join(
        f"Report {r.get('id', 'unknown')} ({r.get('title', 'Untitled')}):\n{r.get('description', '')}"
        for r in context_reports
    )
    prompt = f"Context threat reports:\n{context_text}\n\nQuestion: {question}"
    return await llm_client.complete(prompt, system_prompt=RAG_SYSTEM_PROMPT)
