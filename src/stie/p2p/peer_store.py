from __future__ import annotations

import json
from pathlib import Path

from stie.models.peer import PeerInfo


class PeerStore:
    def __init__(self, path: str = "data/peers.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.peers: dict[str, PeerInfo] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text())
            for peer_id, peer_data in data.items():
                self.peers[peer_id] = PeerInfo(**peer_data)

    def _save(self):
        data = {pid: p.model_dump() for pid, p in self.peers.items()}
        self.path.write_text(json.dumps(data, indent=2, default=str))

    def add_peer(self, peer: PeerInfo):
        self.peers[peer.id] = peer
        self._save()

    def remove_peer(self, peer_id: str):
        self.peers.pop(peer_id, None)
        self._save()

    def get_peer(self, peer_id: str) -> PeerInfo | None:
        return self.peers.get(peer_id)

    def get_known_peers(self, limit: int = 100) -> list[PeerInfo]:
        return sorted(
            self.peers.values(),
            key=lambda p: p.trust_score or 0,
            reverse=True,
        )[:limit]
