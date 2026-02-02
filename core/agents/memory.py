from __future__ import annotations

from sqlalchemy import select

from core.db import models
from core.db.session import get_session


class MemoryAgent:
    def retrieve_recent(self, workspace_id: int) -> dict:
        with get_session() as session:
            research = session.execute(
                select(models.ResearchItem).where(models.ResearchItem.workspace_id == workspace_id)
            ).scalars().all()
            ideas = session.execute(
                select(models.Idea).where(models.Idea.workspace_id == workspace_id)
            ).scalars().all()
            return {
                "research_items": [
                    {
                        "title": item.title,
                        "summary": item.summary,
                        "source_url": item.source_url,
                        "tags": item.tags,
                    }
                    for item in research
                ],
                "ideas": [
                    {
                        "title": idea.title,
                        "description": idea.description,
                        "monetization_score": idea.monetization_score,
                        "justification": idea.justification,
                        "confidence": idea.confidence,
                        "tags": idea.tags,
                    }
                    for idea in ideas
                ],
            }
