from __future__ import annotations

from datetime import datetime
from typing import Any

import stix2
from stix2 import (
    Bundle,
    Report,
)

from stie.models.threat_report import (
    Confidence,
    Severity,
    ThreatReport,
    ThreatType,
    TLPLevel,
)

THREAT_TYPE_TO_STIX_LABEL: dict[ThreatType, str] = {
    ThreatType.SATELLITE_INTRUSION: "satellite-intrusion",
    ThreatType.GNSS_SPOOFING: "gnss-spoofing",
    ThreatType.SIGNAL_JAMMING: "signal-jamming",
    ThreatType.COMMAND_HIJACK: "command-hijack",
    ThreatType.TELEMETRY_TAMPERING: "telemetry-tampering",
    ThreatType.DOS_ATTACK: "dos-attack",
    ThreatType.SUPPLY_CHAIN: "supply-chain",
    ThreatType.PHYSICAL_ATTACK: "physical-attack",
    ThreatType.OTHER: "threat-report",
}


SEVERITY_TO_STIX_CONFIDENCE: dict[Severity, int] = {
    Severity.CRITICAL: 100,
    Severity.HIGH: 75,
    Severity.MEDIUM: 50,
    Severity.LOW: 25,
    Severity.INFO: 10,
}


CONFIDENCE_TO_STIX: dict[Confidence, int] = {
    Confidence.HIGH: 90,
    Confidence.MEDIUM: 50,
    Confidence.LOW: 25,
    Confidence.UNKNOWN: 0,
}


import uuid

def threat_report_to_stix(report: ThreatReport) -> Report:
    labels = [THREAT_TYPE_TO_STIX_LABEL.get(report.threat_type, "threat-report")]
    labels.extend(report.tags)
    if report.gnss_types:
        labels.extend(f"gnss-{g.value}" for g in report.gnss_types)

    external_refs = []
    for ref in report.references:
        external_refs.append(stix2.ExternalReference(source_name="stie", url=ref))

    stix_id = f"report--{uuid.uuid5(uuid.NAMESPACE_DNS, report.id)}"

    return Report(
        id=stix_id,
        name=report.title,
        description=report.description,
        report_types=labels,
        published=report.created_at or datetime.utcnow(),
        confidence=CONFIDENCE_TO_STIX.get(report.confidence, 50),
        object_refs=[],
        allow_custom=True,
    )


def threat_report_from_stix(stix_report: dict[str, Any]) -> dict[str, Any] | None:
    try:
        return {
            "title": stix_report.get("name", "Untitled Report"),
            "description": stix_report.get("description", ""),
            "threat_type": ThreatType.OTHER,
            "severity": Severity.MEDIUM,
            "confidence": Confidence.MEDIUM,
            "tlp_level": TLPLevel.GREEN,
            "tags": stix_report.get("labels", []),
            "references": [
                ref.get("url") for ref in stix_report.get("external_references", []) if ref.get("url")
            ],
        }
    except (KeyError, ValueError):
        return None


def create_stix_bundle(reports: list[ThreatReport]) -> Bundle:
    stix_objects = []
    for report in reports:
        stix_obj = threat_report_to_stix(report)
        stix_objects.append(stix_obj)
    return Bundle(objects=stix_objects, allow_custom=True)
