from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/analytics/summary")
async def analytics_summary():
    raise HTTPException(
        status_code=501,
        detail="Analytics summary not yet implemented",
    )


@router.get("/analytics/trends")
async def analytics_trends(days: int = 30):
    raise HTTPException(
        status_code=501,
        detail="Analytics trends not yet implemented",
    )


@router.get("/analytics/clusters")
async def analytics_clusters():
    raise HTTPException(
        status_code=501,
        detail="Analytics clusters not yet implemented",
    )
