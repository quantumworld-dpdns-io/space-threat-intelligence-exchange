from __future__ import annotations

import logging
from collections.abc import Callable

from stie.config.settings import settings
from stie.models.peer import PeerInfo

logger = logging.getLogger("stie.p2p")


class P2PManager:
    def __init__(self):
        self.enabled = settings.p2p_enabled
        self.port = settings.p2p_port
        self.peers: dict[str, PeerInfo] = {}
        self.message_handlers: dict[str, list[Callable]] = {}
        self._running = False

    async def start(self):
        if not self.enabled:
            logger.info("P2P networking is disabled")
            return
        logger.info("Starting P2P network on port %d", self.port)
        self._running = True

    async def stop(self):
        self._running = False
        logger.info("P2P network stopped")

    async def broadcast_report(self, report_data: dict):
        if not self._running:
            return
        logger.info("Broadcasting report to %d peers", len(self.peers))

    async def request_report(self, report_id: str) -> dict | None:
        return None

    async def discover_peers(self):
        pass

    def register_handler(self, message_type: str, handler: Callable):
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    def get_peer_list(self) -> list[PeerInfo]:
        return list(self.peers.values())

    async def connect_peer(self, multiaddress: str) -> bool:
        return False


p2p_manager = P2PManager()
