from __future__ import annotations

from collections.abc import Callable
from typing import Any

from stie.config.settings import settings

try:
    import weave
    WEAVE_AVAILABLE = True
except ImportError:
    WEAVE_AVAILABLE = False


class WeaveTracker:
    def __init__(self):
        self.enabled = settings.weave_enabled and WEAVE_AVAILABLE
        self._initialized = False

    def initialize(self):
        if self.enabled and not self._initialized:
            try:
                weave.init(settings.wandb_project)
                self._initialized = True
            except Exception:
                self.enabled = False

    def track_llm_call(self, func: Callable) -> Callable:
        if not self.enabled:
            return func
        try:
            return weave.op(func)
        except Exception:
            return func

    async def log_evaluation(self, name: str, score: float, metadata: dict[str, Any] | None = None):
        if not self.enabled:
            return
        try:
            pass
        except Exception:
            pass


weave_tracker = WeaveTracker()
