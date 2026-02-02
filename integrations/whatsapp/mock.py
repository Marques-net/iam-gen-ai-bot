from __future__ import annotations

import structlog

from integrations.whatsapp.base import WhatsAppNotifier

logger = structlog.get_logger()


class MockWhatsAppNotifier(WhatsAppNotifier):
    def send_message(self, recipient_id: str, text: str) -> None:
        logger.info("whatsapp.mock.send", recipient_id=recipient_id, text=text)
