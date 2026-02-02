from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    summary: str
    url: str
    tags: list[str]


class SearchProvider:
    def search(self, query: str, context: dict) -> list[SearchResult]:
        raise NotImplementedError
