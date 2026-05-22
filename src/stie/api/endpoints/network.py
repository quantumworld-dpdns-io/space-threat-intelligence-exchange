from __future__ import annotations

from fastapi import APIRouter, HTTPException

from stie.models.peer import PeerInfo

router = APIRouter()


@router.get("/peers", response_model=list[PeerInfo])
async def list_peers():
    raise HTTPException(
        status_code=501,
        detail="Peer listing not yet implemented",
    )


@router.get("/peers/{peer_id}", response_model=PeerInfo)
async def get_peer(peer_id: str):
    raise HTTPException(
        status_code=501,
        detail="Peer detail not yet implemented",
    )


@router.get("/network/status")
async def network_status():
    raise HTTPException(
        status_code=501,
        detail="Network status not yet implemented",
    )
