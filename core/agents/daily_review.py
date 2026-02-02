from __future__ import annotations

from typing import Any


class DailyReviewAgent:
    def run(self, state: dict) -> list[str]:
        notes: list[str] = []
        research = state.get("research_items", [])
        if not research:
            notes.append("Nenhuma pesquisa recente. Recomendar nova busca de tendências.")
        notes.extend(
            [
                "Sugestão: atualizar títulos com palavras-chave emergentes.",
                "Sugestão: trocar 2 itens do calendário por temas mais atuais.",
                "Sugestão: ajustar CTA para incentivar comentários hoje.",
            ]
        )
        return notes
