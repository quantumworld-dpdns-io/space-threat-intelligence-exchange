from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta

SAMPLE_REPORTS = [
    {
        "title": "GPS Spoofing Attack Detected Over Eastern Mediterranean",
        "description": "On 2026-04-15, multiple maritime vessels in the Eastern Mediterranean reported GPS signal anomalies consistent with spoofing. Vessels reported position discrepancies of 5-15 nautical miles. The spoofing signals appeared to originate from a coastal location and affected both civilian and military GPS receivers in the region. GNSS signal analysis indicated the spoofing targeted civilian GPS L1 frequency.",
        "threat_type": "gnss_spoofing",
        "severity": "high",
        "confidence": "high",
        "tlp_level": "amber",
        "gnss_types": ["gps"],
        "affected_satellites": ["GPS-2F-8", "GPS-2F-9", "GPS-3-SV01"],
        "affected_systems": ["GPS L1 Receiver", "Maritime Navigation Systems"],
        "start_time": "2026-04-15T08:30:00Z",
        "end_time": "2026-04-15T11:45:00Z",
        "observables": [
            {"type": "signal-frequency", "value": "1575.42 MHz"},
            {"type": "geolocation", "value": "33.5N, 28.5E"},
        ],
        "courses_of_action": [
            {"action": "Enable anti-spoofing filters", "description": "Activate receiver autonomous integrity monitoring", "priority": "high"},
            {"action": "Cross-reference with Galileo", "description": "Use Galileo signals for position verification", "priority": "medium"},
        ],
        "tags": ["gps-spoofing", "maritime", "mediterranean", "civilian-infrastructure"],
        "references": ["https://www.gps.gov/spectrum/spoofing/"],
    },
    {
        "title": "Unauthorized Uplink Command Attempt on LEO-Commsat-12",
        "description": "Analysis of telemetry logs from LEO-Commsat-12 revealed multiple unauthorized uplink command attempts originating from an unknown ground station in Central Asia. The commands attempted to modify the satellite's attitude control system parameters. The satellite's intrusion detection system successfully blocked all unauthorized commands. Investigation is ongoing to determine if this is part of a broader campaign targeting LEO communications satellites.",
        "threat_type": "satellite_intrusion",
        "severity": "critical",
        "confidence": "medium",
        "tlp_level": "red",
        "satellite_intrusion_type": "command_injection",
        "affected_satellites": ["LEO-Commsat-12"],
        "affected_systems": ["Attitude Control System", "Uplink Command Processor"],
        "start_time": "2026-05-10T14:22:00Z",
        "end_time": "2026-05-10T14:28:00Z",
        "observables": [
            {"type": "ipv4", "value": "203.0.113.45"},
            {"type": "hash", "value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
        ],
        "courses_of_action": [
            {"action": "Rotate uplink encryption keys", "description": "Generate and distribute new encryption keys", "priority": "critical"},
            {"action": "Increase telemetry monitoring", "description": "24/7 monitoring of all command channels", "priority": "high"},
        ],
        "tags": ["command-injection", "leo", "attitude-control", "intrusion-detection"],
        "references": [],
    },
    {
        "title": "Signal Jamming Affecting Galileo Service in Ukraine Region",
        "description": "Persistent GNSS signal jamming has been detected affecting Galileo satellite signals in a 300km radius centered on eastern Ukraine. The jamming began on 2026-03-01 and has continued intermittently. Multiple GNSS receivers in the region report complete loss of Galileo E1 and E5a signal acquisition during jamming events. The jamming pattern is consistent with ground-based tactical jamming equipment.",
        "threat_type": "signal_jamming",
        "severity": "high",
        "confidence": "high",
        "tlp_level": "green",
        "gnss_types": ["galileo"],
        "affected_satellites": ["Galileo-FOC-FM22", "Galileo-FOC-FM23", "Galileo-FOC-FM24"],
        "affected_systems": ["Galileo E1 Receiver", "Galileo E5a Receiver"],
        "start_time": "2026-03-01T00:00:00Z",
        "end_time": None,
        "observables": [
            {"type": "signal-frequency", "value": "1575.420 MHz (E1)"},
            {"type": "signal-frequency", "value": "1176.450 MHz (E5a)"},
            {"type": "geolocation", "value": "48.5N, 37.5E"},
            {"type": "geolocation-radius", "value": "300 km"},
        ],
        "courses_of_action": [
            {"action": "Deploy alternative PNT sources", "description": "Use inertial navigation and terrestrial backup systems", "priority": "high"},
            {"action": "Report to GNSS service center", "description": "File interference report with Galileo Security Monitoring Centre", "priority": "medium"},
        ],
        "tags": ["jamming", "galileo", "ukraine", "gnss", "tactical-jamming"],
        "references": ["https://www.gsc-europa.eu/notice-advisory-to-galileo-users-nagu"],
    },
]


def generate_seed_data():
    print("Generating seed threat report data...")
    print(f"  Reports: {len(SAMPLE_REPORTS)}")
    for i, report in enumerate(SAMPLE_REPORTS):
        report_id = f"STIE-SEED-{i+1:03d}"
        report["id"] = report_id
        report["author_id"] = "seed-author-001"
        report["version"] = 1
        report["signature"] = None
        report["signature_verified"] = False
        report["created_at"] = datetime.utcnow().isoformat() + "Z"
        report["updated_at"] = report["created_at"]

        filename = f"data/seeds/report_{i+1:03d}.json"
        import os
        os.makedirs("data/seeds", exist_ok=True)
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        print(f"  Created: {filename}")

    print("Seed data generation complete!")


if __name__ == "__main__":
    generate_seed_data()
