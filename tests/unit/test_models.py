from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from stie.models.threat_report import (
    ThreatReportCreate,
    ThreatReport,
    ThreatType,
    Severity,
    Confidence,
    TLPLevel,
    Observable,
    CourseOfAction,
)


class TestThreatReportCreate:
    def test_valid_report(self):
        report = ThreatReportCreate(
            title="Test intrusion",
            description="A test satellite intrusion report",
            threat_type=ThreatType.SATELLITE_INTRUSION,
            severity=Severity.HIGH,
            author_id="author-1",
            tags=["test", "satellite"],
        )
        assert report.title == "Test intrusion"
        assert report.threat_type == ThreatType.SATELLITE_INTRUSION
        assert report.tlp_level == TLPLevel.GREEN

    def test_invalid_empty_title(self):
        with pytest.raises(ValidationError):
            ThreatReportCreate(
                title="",
                description="test",
                threat_type=ThreatType.OTHER,
                severity=Severity.LOW,
                author_id="author-1",
            )

    def test_invalid_empty_description(self):
        with pytest.raises(ValidationError):
            ThreatReportCreate(
                title="Test",
                description="",
                threat_type=ThreatType.OTHER,
                severity=Severity.LOW,
                author_id="author-1",
            )

    def test_with_observables(self):
        report = ThreatReportCreate(
            title="Report with observables",
            description="Test",
            threat_type=ThreatType.GNSS_SPOOFING,
            severity=Severity.CRITICAL,
            author_id="author-1",
            observables=[
                Observable(type="ipv4", value="192.168.1.1"),
                Observable(type="domain", value="malicious.example.com"),
            ],
        )
        assert len(report.observables) == 2
        assert report.observables[0].type == "ipv4"

    def test_with_courses_of_action(self):
        report = ThreatReportCreate(
            title="Report with COA",
            description="Test",
            threat_type=ThreatType.SIGNAL_JAMMING,
            severity=Severity.MEDIUM,
            author_id="author-1",
            courses_of_action=[
                CourseOfAction(
                    action="Update firmware",
                    description="Apply latest firmware patch",
                )
            ],
        )
        assert len(report.courses_of_action) == 1
        assert report.courses_of_action[0].priority == Severity.MEDIUM

    def test_with_gnss_types(self):
        report = ThreatReportCreate(
            title="GNSS spoofing",
            description="Test",
            threat_type=ThreatType.GNSS_SPOOFING,
            severity=Severity.HIGH,
            author_id="author-1",
            gnss_types=[GNSSType.GPS, GNSSType.GALILEO],  # type: ignore
        )
        assert len(report.gnss_types) == 2

    def test_all_fields(self):
        report = ThreatReportCreate(
            title="Comprehensive report",
            description="A comprehensive test report",
            threat_type=ThreatType.SATELLITE_INTRUSION,
            severity=Severity.CRITICAL,
            confidence=Confidence.HIGH,
            tlp_level=TLPLevel.RED,
            satellite_intrusion_type=SatelliteIntrusionType.UPLINK_INTRUSION,  # type: ignore
            gnss_types=[GNSSType.GPS],  # type: ignore
            affected_satellites=["SAT-001", "SAT-002"],
            affected_systems=["TT&C System", "Payload Processor"],
            author_id="author-1",
            tags=["critical", "zero-day"],
            references=["https://example.com/advisory"],
        )
        assert report.severity == Severity.CRITICAL
        assert report.confidence == Confidence.HIGH
        assert report.tlp_level == TLPLevel.RED


class TestThreatReportModel:
    def test_from_attributes(self):
        report = ThreatReport(
            id="STIE-001",
            title="Test",
            description="Test description",
            threat_type=ThreatType.OTHER,
            severity=Severity.INFO,
            author_id="author-1",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        assert report.id == "STIE-001"
        assert report.version == 1
        assert report.signature_verified is False

    def test_with_signature(self):
        report = ThreatReport(
            id="STIE-002",
            title="Signed report",
            description="Test",
            threat_type=ThreatType.SATELLITE_INTRUSION,
            severity=Severity.HIGH,
            author_id="author-1",
            signature="abc123",
            signature_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        assert report.signature == "abc123"
        assert report.signature_verified is True


from stie.models.threat_report import GNSSType, SatelliteIntrusionType
