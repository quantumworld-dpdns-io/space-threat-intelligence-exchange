from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from stie.models.threat_report import (
    ThreatReportCreate,
    ThreatReportResponse,
    ThreatReportSearch,
    ThreatReportUpdate,
)
from stie.storage.database import get_session

router = APIRouter()


@router.post("/reports", response_model=ThreatReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(report: ThreatReportCreate, session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report creation not yet implemented",
    )


@router.get("/reports/{report_id}", response_model=ThreatReportResponse)
async def get_report(report_id: str, session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report retrieval not yet implemented",
    )


@router.get("/reports", response_model=list[ThreatReportResponse])
async def list_reports(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report listing not yet implemented",
    )


@router.patch("/reports/{report_id}", response_model=ThreatReportResponse)
async def update_report(
    report_id: str,
    update: ThreatReportUpdate,
    session: AsyncSession = Depends(get_session),
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report update not yet implemented",
    )


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str, session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report deletion not yet implemented",
    )


@router.post("/reports/search", response_model=list[ThreatReportResponse])
async def search_reports(search: ThreatReportSearch, session: AsyncSession = Depends(get_session)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Report search not yet implemented",
    )


@router.get("/reports/{report_id}/similar", response_model=list[ThreatReportResponse])
async def similar_reports(report_id: str, limit: int = 10):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Similar report search not yet implemented",
    )
