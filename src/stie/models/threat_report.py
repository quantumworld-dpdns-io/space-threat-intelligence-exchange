from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ThreatType(str, Enum):
    SATELLITE_INTRUSION = "satellite_intrusion"
    GNSS_SPOOFING = "gnss_spoofing"
    SIGNAL_JAMMING = "signal_jamming"
    COMMAND_HIJACK = "command_hijack"
    TELEMETRY_TAMPERING = "telemetry_tampering"
    DOS_ATTACK = "dos_attack"
    SUPPLY_CHAIN = "supply_chain"
    PHYSICAL_ATTACK = "physical_attack"
    OTHER = "other"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class TLPLevel(str, Enum):
    RED = "red"
    AMBER = "amber"
    GREEN = "green"
    CLEAR = "clear"


class SatelliteIntrusionType(str, Enum):
    UPLINK_INTRUSION = "uplink_intrusion"
    DOWNLINK_INTERCEPT = "downlink_intercept"
    COMMAND_INJECTION = "command_injection"
    PAYLOAD_TAMPERING = "payload_tampering"
    ORBIT_MANEUVER = "orbit_maneuver"
    TT_C_COMPROMISE = "tt_c_compromise"
    OTHER = "other"


class GNSSType(str, Enum):
    GPS = "gps"
    GLONASS = "glonass"
    GALILEO = "galileo"
    BEIDOU = "beidou"
    IRNSS = "irnss"
    QZSS = "qzss"
    MULTI = "multi"
    OTHER = "other"


class Observable(BaseModel):
    type: str = Field(description="Type of observable (ipv4, domain, hash, url, etc.)")
    value: str = Field(description="The observable value")


class CourseOfAction(BaseModel):
    action: str = Field(description="Recommended action")
    description: str = Field(description="Detailed description of the action")
    priority: Severity = Field(default=Severity.MEDIUM)


class ThreatReportBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1)
    threat_type: ThreatType
    severity: Severity
    confidence: Confidence = Field(default=Confidence.MEDIUM)
    tlp_level: TLPLevel = Field(default=TLPLevel.GREEN)

    satellite_intrusion_type: Optional[SatelliteIntrusionType] = None
    gnss_types: list[GNSSType] = Field(default_factory=list)

    affected_satellites: list[str] = Field(default_factory=list)
    affected_systems: list[str] = Field(default_factory=list)

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    observables: list[Observable] = Field(default_factory=list)
    courses_of_action: list[CourseOfAction] = Field(default_factory=list)

    tags: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)


class ThreatReportCreate(ThreatReportBase):
    author_id: str
    organization_id: Optional[str] = None


class ThreatReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Severity] = None
    confidence: Optional[Confidence] = None
    tlp_level: Optional[TLPLevel] = None
    observables: Optional[list[Observable]] = None
    courses_of_action: Optional[list[CourseOfAction]] = None
    tags: Optional[list[str]] = None


class ThreatReport(ThreatReportBase):
    id: str
    author_id: str
    organization_id: Optional[str] = None
    signature: Optional[str] = None
    signature_verified: bool = False
    created_at: datetime
    updated_at: datetime
    version: int = 1

    class Config:
        from_attributes = True


class ThreatReportResponse(ThreatReport):
    pass


class ThreatReportSearch(BaseModel):
    query: Optional[str] = None
    threat_type: Optional[ThreatType] = None
    severity: Optional[Severity] = None
    tlp_level: Optional[TLPLevel] = None
    confidence: Optional[Confidence] = None
    tags: Optional[list[str]] = None
    author_id: Optional[str] = None
    start_time_from: Optional[datetime] = None
    start_time_to: Optional[datetime] = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)
