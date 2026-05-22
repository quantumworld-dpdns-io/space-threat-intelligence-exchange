from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PeerStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class PeerInfo(BaseModel):
    id: str
    public_key: str
    multiaddresses: list[str]
    status: PeerStatus = PeerStatus.UNKNOWN
    version: str = "0.1.0"
    capabilities: list[str] = Field(default_factory=list)
    last_seen: Optional[datetime] = None
    latency_ms: Optional[float] = None
    report_count: int = 0
    trust_score: float = 0.0

    class Config:
        from_attributes = True
