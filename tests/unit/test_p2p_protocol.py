from __future__ import annotations

import pytest

from stie.p2p.protocol import (
    MessageType,
    encode_message,
    decode_message,
)


class TestP2PProtocol:
    def test_encode_decode_ping(self):
        payload = {"timestamp": 1234567890}
        data = encode_message(MessageType.PING, payload)
        msg_type, decoded = decode_message(data)
        assert msg_type == MessageType.PING
        assert decoded["timestamp"] == 1234567890

    def test_encode_decode_report(self):
        payload = {
            "report_id": "STIE-001",
            "title": "Test intrusion",
            "severity": "high",
        }
        data = encode_message(MessageType.REPORT_PUBLISH, payload)
        msg_type, decoded = decode_message(data)
        assert msg_type == MessageType.REPORT_PUBLISH
        assert decoded["report_id"] == "STIE-001"
        assert decoded["severity"] == "high"

    def test_all_message_types(self):
        for msg_type in MessageType:
            payload = {"type": msg_type.name}
            data = encode_message(msg_type, payload)
            decoded_type, decoded = decode_message(data)
            assert decoded_type == msg_type
            assert decoded["type"] == msg_type.name

    def test_empty_payload(self):
        data = encode_message(MessageType.PING, {})
        msg_type, decoded = decode_message(data)
        assert msg_type == MessageType.PING
        assert decoded == {}

    def test_nested_payload(self):
        payload = {
            "report": {
                "id": "STIE-001",
                "observables": [
                    {"type": "ipv4", "value": "10.0.0.1"},
                ],
            }
        }
        data = encode_message(MessageType.REPORT_RESPONSE, payload)
        msg_type, decoded = decode_message(data)
        assert decoded["report"]["observables"][0]["value"] == "10.0.0.1"
