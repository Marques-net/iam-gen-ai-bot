from __future__ import annotations

from integrations.search.base import SearchProvider, SearchResult


class MockSearchProvider(SearchProvider):
    def search(self, query: str, context: dict) -> list[SearchResult]:
        return [
            SearchResult(
                title=f"Tendência simulada para {query}",
                summary="Resumo sintético com base em dados simulados.",
                url="https://example.com/trends/mock",
                tags=["mock", "trend"],
            )
        ]
