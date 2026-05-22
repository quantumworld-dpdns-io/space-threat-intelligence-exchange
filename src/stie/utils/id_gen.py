from __future__ import annotations

import time
import uuid


def generate_report_id() -> str:
    timestamp = int(time.time() * 1000)
    unique = uuid.uuid4().hex[:12]
    return f"STIE-{timestamp:013d}-{unique}"


def generate_identity_id() -> str:
    return f"ID-{uuid.uuid4().hex[:16]}"


def generate_campaign_id() -> str:
    return f"CAM-{uuid.uuid4().hex[:12]}"


def generate_peer_id() -> str:
    return f"PEER-{uuid.uuid4().hex[:16]}"
