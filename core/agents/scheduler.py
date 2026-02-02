from __future__ import annotations

import calendar
import datetime as dt


class SchedulerAgent:
    def run(self, state: dict) -> list[dict]:
        from core.db import repositories
        from core.db.session import get_session

        today = dt.date.today()
        year = today.year
        month = today.month
        _, days_in_month = calendar.monthrange(year, month)

        ideas = state.get("ideas", [])
        if not ideas:
            return []

        items: list[dict] = []
        idea_index = 0
        for day in range(1, days_in_month + 1):
            for _ in range(self._items_per_day(state)):
                idea = ideas[idea_index % len(ideas)]
                idea_index += 1
                items.append(
                    {
                        "date": dt.date(year, month, day),
                        "title": idea["title"],
                        "format": state["parameters"].get("content_type", "shorts"),
                        "monetization_score": idea["monetization_score"],
                        "justification": idea["justification"],
                        "research_sources": [item["source_url"] for item in state.get("research_items", [])],
                    }
                )

        with get_session() as session:
            repositories.save_calendar_items(
                session,
                workspace_id=state["workspace_id"],
                campaign_id=state["campaign_id"],
                items=items,
            )
        return items

    def _items_per_day(self, state: dict) -> int:
        frequency = state["parameters"].get("frequency", "1 por dia")
        if "2" in frequency:
            return 2
        return 1
