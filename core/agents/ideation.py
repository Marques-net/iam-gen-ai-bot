from __future__ import annotations

import random

from core.db import repositories
from core.db.session import get_session


class IdeationAgent:
    def run(self, state: dict) -> list[dict]:
        ideas = []
        base_topics = [item["title"] for item in state.get("research_items", [])]
        if not base_topics:
            base_topics = ["Ideias evergreen", "Dicas práticas", "Curiosidades"]

        for topic in base_topics:
            monetization_score = round(random.uniform(0.4, 0.85), 2)
            ideas.append(
                {
                    "title": f"{topic} - ângulo novo",
                    "description": "Explorar o tema com abordagem alinhada ao público.",
                    "monetization_score": monetization_score,
                    "justification": "Heurística baseada em tendência, interesse e potencial de retenção.",
                    "confidence": round(random.uniform(0.5, 0.9), 2),
                    "tags": ["trend", "mvp"],
                }
            )

        with get_session() as session:
            repositories.save_ideas(
                session,
                workspace_id=state["workspace_id"],
                campaign_id=state["campaign_id"],
                ideas=ideas,
            )
        return ideas
