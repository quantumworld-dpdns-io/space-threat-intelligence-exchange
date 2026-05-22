from __future__ import annotations

import json
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.exceptions import InvalidSignature

from stie.crypto.keys import (
    deserialize_private_key,
    deserialize_public_key,
    serialize_public_key,
    get_key_fingerprint,
)


def sign_report(report_data: dict, private_key_pem: str) -> str:
    private_key = deserialize_private_key(private_key_pem)
    canonical = json.dumps(report_data, sort_keys=True, separators=(",", ":")).encode()
    signature = private_key.sign(canonical)
    return signature.hex()


def verify_report_signature(
    report_data: dict,
    signature_hex: str,
    public_key_pem: str,
) -> bool:
    try:
        public_key = deserialize_public_key(public_key_pem)
        canonical = json.dumps(report_data, sort_keys=True, separators=(",", ":")).encode()
        signature = bytes.fromhex(signature_hex)
        public_key.verify(signature, canonical)
        return True
    except (InvalidSignature, ValueError, Exception):
        return False


def create_signed_envelope(
    report_data: dict,
    private_key_pem: str,
    public_key_pem: str,
) -> dict:
    signature = sign_report(report_data, private_key_pem)
    return {
        "report": report_data,
        "signature": signature,
        "signer_fingerprint": get_key_fingerprint(deserialize_public_key(public_key_pem)),
        "signer_public_key": public_key_pem,
    }


def verify_signed_envelope(envelope: dict) -> tuple[bool, Optional[str]]:
    try:
        report_data = envelope["report"]
        signature = envelope["signature"]
        public_key_pem = envelope["signer_public_key"]
        valid = verify_report_signature(report_data, signature, public_key_pem)
        if valid:
            return True, get_key_fingerprint(deserialize_public_key(public_key_pem))
        return False, None
    except (KeyError, ValueError, Exception):
        return False, None
