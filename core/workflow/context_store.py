from __future__ import annotations

import json
from typing import Any

import redis

from core.settings import settings


class ContextStore:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def get(self, sender_id: str) -> dict[str, Any]:
        raw = self.client.get(f"ctx:{sender_id}")
        if not raw:
            return {}
        return json.loads(raw)

    def set(self, sender_id: str, data: dict[str, Any]) -> None:
        self.client.set(f"ctx:{sender_id}", json.dumps(data))
