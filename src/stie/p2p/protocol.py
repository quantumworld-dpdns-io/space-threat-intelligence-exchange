from __future__ import annotations

from enum import IntEnum
from typing import Any


class MessageType(IntEnum):
    PING = 0
    PONG = 1
    REPORT_PUBLISH = 2
    REPORT_REQUEST = 3
    REPORT_RESPONSE = 4
    PEER_DISCOVERY = 5
    PEER_LIST = 6
    SYNC_REQUEST = 7
    SYNC_RESPONSE = 8


MESSAGE_HEADER_SIZE = 4


def encode_message(message_type: MessageType, payload: dict[str, Any]) -> bytes:
    import json
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    header = message_type.to_bytes(MESSAGE_HEADER_SIZE, byteorder="big")
    length = len(payload_bytes).to_bytes(MESSAGE_HEADER_SIZE, byteorder="big")
    return header + length + payload_bytes


def decode_message(data: bytes) -> tuple[MessageType, dict[str, Any]]:
    import json
    message_type = MessageType(int.from_bytes(data[:MESSAGE_HEADER_SIZE], byteorder="big"))
    payload_length = int.from_bytes(data[MESSAGE_HEADER_SIZE : MESSAGE_HEADER_SIZE * 2], byteorder="big")
    payload = json.loads(data[MESSAGE_HEADER_SIZE * 2 : MESSAGE_HEADER_SIZE * 2 + payload_length])
    return message_type, payload
