from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from stie.models.threat_report import Severity, Confidence


class CampaignBase(BaseModel):
    name: str = Field(min_length=1, max_length=300)
    description: str
    severity: Severity = Field(default=Severity.MEDIUM)
    confidence: Confidence = Field(default=Confidence.MEDIUM)
    actor: Optional[str] = None
    motivation: Optional[str] = None
    target_sectors: list[str] = Field(default_factory=list)
    target_regions: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class CampaignCreate(CampaignBase):
    report_ids: list[str] = Field(default_factory=list)


class Campaign(CampaignBase):
    id: str
    report_ids: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    version: int = 1
    is_active: bool = True

    class Config:
        from_attributes = True


class CampaignResponse(Campaign):
    report_count: int = 0
