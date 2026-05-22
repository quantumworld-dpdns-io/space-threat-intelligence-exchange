from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class STIXExportRequest(BaseModel):
    report_ids: list[str]
    format: str = "json"


@router.post("/stix/export")
async def stix_export(request: STIXExportRequest):
    raise HTTPException(
        status_code=501,
        detail="STIX export not yet implemented",
    )


@router.post("/stix/import")
async def stix_import():
    raise HTTPException(
        status_code=501,
        detail="STIX import not yet implemented",
    )


@router.get("/feeds/stix")
async def stix_feed(collection_id: str = "default"):
    raise HTTPException(
        status_code=501,
        detail="STIX feed not yet implemented",
    )
