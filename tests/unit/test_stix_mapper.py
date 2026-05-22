from __future__ import annotations

from datetime import datetime

import pytest

from stie.models.threat_report import ThreatReport, ThreatType, Severity, Confidence, TLPLevel
from stie.stix.mapper import (
    threat_report_to_stix,
    threat_report_from_stix,
    create_stix_bundle,
    THREAT_TYPE_TO_STIX_LABEL,
)


class TestSTIXMapper:
    @pytest.fixture
    def sample_report(self):
        return ThreatReport(
            id="STIE-001",
            title="Satellite Intrusion Detected",
            description="A sophisticated intrusion targeting telemetry systems",
            threat_type=ThreatType.SATELLITE_INTRUSION,
            severity=Severity.HIGH,
            confidence=Confidence.MEDIUM,
            tlp_level=TLPLevel.AMBER,
            author_id="author-1",
            tags=["intrusion", "telemetry"],
            references=["https://example.com/ref1"],
            gnss_types=[],
            affected_satellites=["SAT-001"],
            affected_systems=[],
            observables=[],
            courses_of_action=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def test_report_to_stix(self, sample_report):
        stix_report = threat_report_to_stix(sample_report)
        assert stix_report.name == "Satellite Intrusion Detected"
        assert stix_report.type == "report"
        assert "satellite-intrusion" in stix_report.report_types

    def test_report_to_stix_labels(self, sample_report):
        stix_report = threat_report_to_stix(sample_report)
        assert "intrusion" in stix_report.report_types
        assert "telemetry" in stix_report.report_types

    def test_report_to_stix_external_refs(self, sample_report):
        stix_report = threat_report_to_stix(sample_report)
        assert stix_report.external_references is not None
        assert len(stix_report.external_references) == 1
        assert stix_report.external_references[0].url == "https://example.com/ref1"

    def test_report_to_stix_confidence(self, sample_report):
        stix_report = threat_report_to_stix(sample_report)
        assert stix_report.confidence == 50

    def test_stix_round_trip(self, sample_report):
        stix_report = threat_report_to_stix(sample_report)
        stix_dict = {
            "name": stix_report.name,
            "description": stix_report.description,
            "report_types": stix_report.report_types,
            "external_references": stix_report.external_references,
        }
        result = threat_report_from_stix(stix_dict)
        assert result is not None
        assert result["title"] == "Satellite Intrusion Detected"

    def test_create_bundle(self, sample_report):
        bundle = create_stix_bundle([sample_report])
        assert bundle.type == "bundle"
        assert len(bundle.objects) == 1
