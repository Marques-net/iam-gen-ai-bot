from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    provider: str


class LLMProvider:
    def chat(self, prompt: str, context: dict) -> LLMResponse:
        raise NotImplementedError
