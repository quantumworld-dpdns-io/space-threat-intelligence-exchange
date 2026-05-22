from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Organization(BaseModel):
    id: str
    name: str
    description: str | None = None
    sector: str = "space"
    country: str | None = None
    created_at: datetime


class IdentityBase(BaseModel):
    display_name: str = Field(min_length=1, max_length=200)
    email: str | None = None
    organization_id: str | None = None
    public_key: str = Field(description="Ed25519 public key in PEM format")
    role: str = Field(default="analyst")


class IdentityCreate(IdentityBase):
    pass


class Identity(IdentityBase):
    id: str
    fingerprint: str
    created_at: datetime
    updated_at: datetime
    last_seen: datetime | None = None
    is_active: bool = True

    class Config:
        from_attributes = True


class IdentityResponse(Identity):
    pass
