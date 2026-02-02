from __future__ import annotations

import re
from dataclasses import dataclass

from core.workflow.messages import IncomingMessage


@dataclass
class IntakeResult:
    action: str
    workspace_name: str | None = None
    campaign_name: str | None = None
    parameters: dict | None = None
    missing_fields: list[str] | None = None
    response_text: str | None = None


class IntakeAgent:
    def run(self, message: IncomingMessage, context: dict) -> IntakeResult:
        text = message.text.strip().lower()
        if text.startswith("novo projeto"):
            name = text.replace("novo projeto", "").strip() or "default"
            return IntakeResult(action="new_project", campaign_name=name)
        if text.startswith("trocar projeto"):
            name = text.replace("trocar projeto", "").strip() or "default"
            return IntakeResult(action="switch_project", campaign_name=name)
        if text == "parametros":
            return IntakeResult(action="show_parameters")
        if text in {"gerar agenda mensal", "gerar agenda"}:
            return IntakeResult(action="generate_monthly")
        if text in {"revisar hoje", "revisão hoje", "revisao hoje"}:
            return IntakeResult(action="daily_review")
        if text.startswith("aprovar"):
            return IntakeResult(action="approve", response_text=text)
        if text.startswith("reprovar"):
            return IntakeResult(action="reject", response_text=text)

        parameters = context.get("parameters", {})
        updates = self._extract_parameters(text)
        parameters.update({k: v for k, v in updates.items() if v})
        missing = [
            field
            for field in ["channel_type", "content_type", "frequency", "language"]
            if field not in parameters
        ]
        response = None
        if missing:
            response = (
                "Faltam parâmetros: "
                + ", ".join(missing)
                + ". Ex: canal infantil, shorts, 2 por dia, idioma pt-BR."
            )
        return IntakeResult(
            action="update_parameters",
            parameters=parameters,
            missing_fields=missing,
            response_text=response,
        )

    def _extract_parameters(self, text: str) -> dict:
        channel_type = None
        if "infantil" in text:
            channel_type = "infantil"
        elif "adulto" in text:
            channel_type = "adulto"
        elif "pop" in text:
            channel_type = "pop"
        elif "geek" in text:
            channel_type = "geek"

        content_type = None
        if "short" in text:
            content_type = "shorts"
        elif "video longo" in text or "vídeo longo" in text:
            content_type = "long"
        elif "instagram" in text:
            content_type = "instagram"

        frequency = None
        freq_match = re.search(r"(\d+)\s*(shorts|vídeos|videos)\s*/?\s*(dia|semana)", text)
        if freq_match:
            quantity = freq_match.group(1)
            period = freq_match.group(3)
            frequency = f"{quantity} por {period}"

        language = None
        if "pt-br" in text or "portugues" in text or "português" in text:
            language = "pt-BR"
        if "en" in text or "ingl" in text:
            language = "en-US"

        return {
            "channel_type": channel_type,
            "content_type": content_type,
            "frequency": frequency,
            "language": language,
        }
