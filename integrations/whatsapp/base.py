from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WhatsAppMessage:
    sender_id: str
    text: str


class WhatsAppNotifier:
    def send_message(self, recipient_id: str, text: str) -> None:
        raise NotImplementedError
