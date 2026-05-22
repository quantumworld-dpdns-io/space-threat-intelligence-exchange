from __future__ import annotations

import pytest

from stie.crypto.keys import (
    generate_key_pair,
    serialize_private_key,
    serialize_public_key,
    deserialize_private_key,
    deserialize_public_key,
    get_key_fingerprint,
)
from stie.crypto.signing import (
    sign_report,
    verify_report_signature,
    create_signed_envelope,
    verify_signed_envelope,
)


class TestKeyGeneration:
    def test_generate_key_pair(self):
        priv, pub = generate_key_pair()
        assert priv is not None
        assert pub is not None

    def test_serialize_deserialize_private(self):
        priv, pub = generate_key_pair()
        pem = serialize_private_key(priv)
        assert pem.startswith("-----BEGIN PRIVATE KEY-----")
        loaded = deserialize_private_key(pem)
        assert loaded is not None

    def test_serialize_deserialize_public(self):
        priv, pub = generate_key_pair()
        pem = serialize_public_key(pub)
        assert pem.startswith("-----BEGIN PUBLIC KEY-----")
        loaded = deserialize_public_key(pem)
        assert loaded is not None

    def test_key_fingerprint(self):
        priv, pub = generate_key_pair()
        fp = get_key_fingerprint(pub)
        assert len(fp) == 16
        assert isinstance(fp, str)

    def test_multiple_keys_different_fingerprints(self):
        _, pub1 = generate_key_pair()
        _, pub2 = generate_key_pair()
        fp1 = get_key_fingerprint(pub1)
        fp2 = get_key_fingerprint(pub2)
        assert fp1 != fp2


class TestSigning:
    def test_sign_and_verify(self):
        priv, pub = generate_key_pair()
        priv_pem = serialize_private_key(priv)
        pub_pem = serialize_public_key(pub)

        data = {"title": "Test Report", "threat_type": "satellite_intrusion"}
        signature = sign_report(data, priv_pem)
        assert len(signature) > 0

        valid = verify_report_signature(data, signature, pub_pem)
        assert valid is True

    def test_verify_wrong_key(self):
        priv, _ = generate_key_pair()
        _, wrong_pub = generate_key_pair()

        priv_pem = serialize_private_key(priv)
        wrong_pem = serialize_public_key(wrong_pub)

        data = {"title": "Test"}
        signature = sign_report(data, priv_pem)

        valid = verify_report_signature(data, signature, wrong_pem)
        assert valid is False

    def test_verify_tampered_data(self):
        priv, pub = generate_key_pair()
        priv_pem = serialize_private_key(priv)
        pub_pem = serialize_public_key(pub)

        data = {"title": "Original"}
        signature = sign_report(data, priv_pem)

        tampered = {"title": "Tampered"}
        valid = verify_report_signature(tampered, signature, pub_pem)
        assert valid is False

    def test_signed_envelope(self):
        priv, pub = generate_key_pair()
        priv_pem = serialize_private_key(priv)
        pub_pem = serialize_public_key(pub)

        data = {"title": "Envelope Test", "severity": "high"}
        envelope = create_signed_envelope(data, priv_pem, pub_pem)

        assert "report" in envelope
        assert "signature" in envelope
        assert "signer_public_key" in envelope
        assert "signer_fingerprint" in envelope
        assert envelope["report"] == data

        valid, fp = verify_signed_envelope(envelope)
        assert valid is True
        assert fp is not None

    def test_verify_tampered_envelope(self):
        priv, pub = generate_key_pair()
        priv_pem = serialize_private_key(priv)
        pub_pem = serialize_public_key(pub)

        data = {"title": "Test"}
        envelope = create_signed_envelope(data, priv_pem, pub_pem)
        envelope["report"]["title"] = "Tampered"

        valid, _ = verify_signed_envelope(envelope)
        assert valid is False

    def test_verify_invalid_envelope(self):
        valid, _ = verify_signed_envelope({})
        assert valid is False

        valid, _ = verify_signed_envelope({"report": {}, "signature": "bad"})
        assert valid is False
