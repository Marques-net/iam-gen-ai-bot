from __future__ import annotations

import json

from core.cache import PromptCache
from core.db import repositories
from core.db.session import get_session
from integrations.factory import get_search_provider


class ResearchAgent:
    def run(self, state: dict) -> list[dict]:
        provider = get_search_provider()
        cache = PromptCache()
        query = state["parameters"].get("content_topic", "tendências do canal")
        cache_key = cache.build_key({"query": query, "workspace": state["workspace_id"]})
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)

        results = provider.search(query, context=state)
        items = [
            {
                "title": result.title,
                "summary": result.summary,
                "source_url": result.url,
                "tags": result.tags,
            }
            for result in results
        ]
        cache.set(cache_key, json.dumps(items))
        with get_session() as session:
            repositories.record_prompt_cache(
                session,
                prompt_hash=cache_key,
                provider="search",
                metadata={"query": query},
                workspace_id=state["workspace_id"],
            )
            repositories.save_research_items(
                session,
                workspace_id=state["workspace_id"],
                campaign_id=state["campaign_id"],
                items=items,
            )
        return items
