from __future__ import annotations


class EditorGuideAgent:
    def run(self, state: dict) -> list[dict]:
        guides = []
        tool = state.get("parameters", {}).get("editing_tool", "CapCut")
        for item in state.get("calendar_items", [])[:5]:
            guides.append(
                {
                    "calendar_item_id": item.get("id"),
                    "tool": tool,
                    "steps": [
                        "Importar clipes e organizar por cena.",
                        "Adicionar legendas automáticas e revisar pontuação.",
                        "Inserir trilha livre/licenciada e ajustar volume.",
                        "Exportar em formato recomendado para o canal.",
                    ],
                }
            )
        return guides
