from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IncomingMessage:
    sender_id: str
    text: str
    workspace_name: str | None = None
    campaign_name: str | None = None
