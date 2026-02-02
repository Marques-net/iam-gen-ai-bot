from __future__ import annotations

from core.db import repositories
from core.db.session import get_session


class StoryboardAgent:
    def run(self, state: dict) -> list[dict]:
        storyboards = []
        for item in state.get("calendar_items", [])[:5]:
            frames = [
                {
                    "frame": 1,
                    "description": "Cena de abertura com texto chamativo.",
                    "prompt": "Ilustração original, sem marcas registradas, estilo moderno.",
                },
                {
                    "frame": 2,
                    "description": "Demonstração do ponto principal.",
                    "prompt": "Cena educativa, elementos abstratos, paleta vibrante.",
                },
                {
                    "frame": 3,
                    "description": "CTA final com elementos visuais simples.",
                    "prompt": "Tela final clean, sem logos, espaço para texto.",
                },
            ]
            storyboards.append({"calendar_item_id": item.get("id"), "frames": frames})
        with get_session() as session:
            repositories.save_storyboards(
                session,
                workspace_id=state["workspace_id"],
                campaign_id=state["campaign_id"],
                storyboards=storyboards,
            )
        return storyboards
