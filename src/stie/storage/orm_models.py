from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from stie.storage.database import Base


class ThreatReportModel(Base):
    __tablename__ = "threat_reports"

    id = Column(String(64), primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    threat_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    confidence = Column(String(20), default="medium")
    tlp_level = Column(String(20), default="green")

    satellite_intrusion_type = Column(String(50), nullable=True)
    gnss_types = Column(JSON, default=list)

    affected_satellites = Column(JSON, default=list)
    affected_systems = Column(JSON, default=list)

    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    observables = Column(JSON, default=list)
    courses_of_action = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    references = Column(JSON, default=list)

    author_id = Column(String(64), ForeignKey("identities.id"), nullable=False)
    organization_id = Column(String(64), nullable=True)

    signature = Column(Text, nullable=True)
    signature_verified = Column(Boolean, default=False)

    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("IdentityModel", back_populates="reports")


class IdentityModel(Base):
    __tablename__ = "identities"

    id = Column(String(64), primary_key=True)
    display_name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=True)
    organization_id = Column(String(64), nullable=True)
    public_key = Column(Text, nullable=False)
    fingerprint = Column(String(64), nullable=False, unique=True)
    role = Column(String(50), default="analyst")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = Column(DateTime, nullable=True)

    reports = relationship("ThreatReportModel", back_populates="author")


class CampaignModel(Base):
    __tablename__ = "campaigns"

    id = Column(String(64), primary_key=True)
    name = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")
    confidence = Column(String(20), default="medium")
    actor = Column(String(200), nullable=True)
    motivation = Column(String(500), nullable=True)
    target_sectors = Column(JSON, default=list)
    target_regions = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    report_ids = Column(JSON, default=list)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
