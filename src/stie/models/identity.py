from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Organization(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    sector: str = "space"
    country: Optional[str] = None
    created_at: datetime


class IdentityBase(BaseModel):
    display_name: str = Field(min_length=1, max_length=200)
    email: Optional[str] = None
    organization_id: Optional[str] = None
    public_key: str = Field(description="Ed25519 public key in PEM format")
    role: str = Field(default="analyst")


class IdentityCreate(IdentityBase):
    pass


class Identity(IdentityBase):
    id: str
    fingerprint: str
    created_at: datetime
    updated_at: datetime
    last_seen: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class IdentityResponse(Identity):
    pass
