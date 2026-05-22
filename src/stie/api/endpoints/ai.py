from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class EnrichRequest(BaseModel):
    report_id: str


class SummarizeRequest(BaseModel):
    report_id: str


class QARequest(BaseModel):
    question: str
    context_report_ids: list[str] = []


@router.post("/enrich")
async def enrich_report(request: EnrichRequest):
    raise HTTPException(
        status_code=501,
        detail="AI enrichment not yet implemented",
    )


@router.post("/summarize")
async def summarize_report(request: SummarizeRequest):
    raise HTTPException(
        status_code=501,
        detail="AI summarization not yet implemented",
    )


@router.post("/qa")
async def ask_question(request: QARequest):
    raise HTTPException(
        status_code=501,
        detail="AI Q&A not yet implemented",
    )
