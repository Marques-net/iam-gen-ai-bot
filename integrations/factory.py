from __future__ import annotations

from core.settings import settings
from integrations.llm.base import LLMProvider
from integrations.llm.mock import MockLLMProvider
from integrations.search.base import SearchProvider
from integrations.search.mock import MockSearchProvider
from integrations.whatsapp.base import WhatsAppNotifier
from integrations.whatsapp.mock import MockWhatsAppNotifier


def get_llm_provider() -> LLMProvider:
    return MockLLMProvider()


def get_search_provider() -> SearchProvider:
    return MockSearchProvider()


def get_whatsapp_notifier() -> WhatsAppNotifier:
    return MockWhatsAppNotifier()
