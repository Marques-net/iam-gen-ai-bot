from __future__ import annotations

import hashlib
import json
from typing import Any

import redis

from core.settings import settings


class PromptCache:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

    def build_key(self, payload: dict[str, Any]) -> str:
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def set(self, key: str, value: str, ttl_seconds: int = 86400) -> None:
        self.client.setex(key, ttl_seconds, value)
