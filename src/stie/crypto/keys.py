from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitypes.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)


def generate_key_pair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key: Ed25519PrivateKey) -> str:
    return private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    ).decode()


def serialize_public_key(public_key: Ed25519PublicKey) -> str:
    return public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode()


def deserialize_private_key(pem_data: str) -> Ed25519PrivateKey:
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    return load_pem_private_key(pem_data.encode(), password=None)


def deserialize_public_key(pem_data: str) -> Ed25519PublicKey:
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    return load_pem_public_key(pem_data.encode())


def get_key_fingerprint(public_key: Ed25519PublicKey) -> str:
    import hashlib
    key_bytes = public_key.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    return hashlib.sha256(key_bytes).hexdigest()[:16]
