from __future__ import annotations

from core.db import repositories
from core.db.session import get_session


class ScriptWriterAgent:
    def run(self, state: dict) -> list[dict]:
        scripts = []
        for item in state.get("calendar_items", [])[:5]:
            content = (
                f"Título: {item['title']}\n"
                "Abertura: Hook rápido + promessa.\n"
                "Corpo: 3 pontos principais, linguagem simples e direta.\n"
                "CTA: Incentivar inscrição/curtida sem prometer monetização.\n"
                "Compliance: não usar IP protegido; sugerir trilhas licenciadas."
            )
            scripts.append(
                {
                    "calendar_item_id": item.get("id"),
                    "script_type": "youtube",
                    "content": content,
                }
            )
        with get_session() as session:
            repositories.save_scripts(
                session,
                workspace_id=state["workspace_id"],
                campaign_id=state["campaign_id"],
                scripts=scripts,
            )
        return scripts
