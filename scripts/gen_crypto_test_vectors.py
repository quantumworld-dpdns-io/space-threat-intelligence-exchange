#!/usr/bin/env python3
"""Generate cryptographic test vectors for CI/testing."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from stie.crypto.keys import generate_key_pair, serialize_private_key, serialize_public_key
from stie.crypto.signing import create_signed_envelope

OUTPUT_DIR = Path("data/test_vectors")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate():
    priv, pub = generate_key_pair()
    priv_pem = serialize_private_key(priv)
    pub_pem = serialize_public_key(pub)

    (OUTPUT_DIR / "test_private.pem").write_text(priv_pem)
    (OUTPUT_DIR / "test_public.pem").write_text(pub_pem)

    report = {
        "title": "Test Vector Report",
        "description": "A test report for cryptographic verification",
        "threat_type": "satellite_intrusion",
        "severity": "medium",
    }

    envelope = create_signed_envelope(report, priv_pem, pub_pem)
    (OUTPUT_DIR / "test_signed_report.json").write_text(
        json.dumps(envelope, indent=2)
    )

    print(f"Test vectors generated in {OUTPUT_DIR}")
    print(f"  Private key: test_private.pem")
    print(f"  Public key:  test_public.pem")
    print(f"  Signed report: test_signed_report.json")


if __name__ == "__main__":
    generate()
