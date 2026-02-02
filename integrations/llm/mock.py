from __future__ import annotations

from integrations.llm.base import LLMProvider, LLMResponse


class MockLLMProvider(LLMProvider):
    def chat(self, prompt: str, context: dict) -> LLMResponse:
        summary = prompt[:200].replace("\n", " ")
        return LLMResponse(content=f"[MOCK LLM] {summary}", provider="mock")
