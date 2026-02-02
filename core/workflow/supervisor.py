from __future__ import annotations

import uuid

import structlog

from core.agents.daily_review import DailyReviewAgent
from core.agents.editor_guide import EditorGuideAgent
from core.agents.ideation import IdeationAgent
from core.agents.intake import IntakeAgent
from core.agents.memory import MemoryAgent
from core.agents.research import ResearchAgent
from core.agents.scheduler import SchedulerAgent
from core.agents.script_writer import ScriptWriterAgent
from core.agents.storyboard import StoryboardAgent
from core.db import repositories
from core.db.session import get_session
from core.workflow.context_store import ContextStore
from core.workflow.messages import IncomingMessage
from core.workflow.state import WorkflowState
from integrations.factory import get_whatsapp_notifier

logger = structlog.get_logger()


class SupervisorAgent:
    def __init__(self) -> None:
        self.intake = IntakeAgent()
        self.research = ResearchAgent()
        self.ideation = IdeationAgent()
        self.scheduler = SchedulerAgent()
        self.script_writer = ScriptWriterAgent()
        self.storyboard = StoryboardAgent()
        self.editor_guide = EditorGuideAgent()
        self.daily_review = DailyReviewAgent()
        self.memory = MemoryAgent()
        self.context_store = ContextStore()
        self.notifier = get_whatsapp_notifier()

    def handle_message(self, message: IncomingMessage) -> dict:
        context = self.context_store.get(message.sender_id)
        result = self.intake.run(message, context)

        if result.action in {"new_project", "switch_project"}:
            context["campaign_name"] = result.campaign_name
            if "workspace_name" not in context:
                context["workspace_name"] = message.workspace_name or "default"
            self.context_store.set(message.sender_id, context)
            self.notifier.send_message(
                message.sender_id,
                f"Projeto ativo: {context['campaign_name']} (workspace {context['workspace_name']}).",
            )
            return {"status": "ok"}

        if result.action == "show_parameters":
            self.notifier.send_message(message.sender_id, f"Parâmetros atuais: {context.get('parameters', {})}")
            return {"status": "ok"}

        if result.action == "update_parameters":
            context["parameters"] = result.parameters or context.get("parameters", {})
            self.context_store.set(message.sender_id, context)
            if result.response_text:
                self.notifier.send_message(message.sender_id, result.response_text)
            return {"status": "ok"}

        if result.action == "generate_monthly":
            return self.run_monthly_generation(message.sender_id, context)

        if result.action == "daily_review":
            return self.run_daily_review(message.sender_id, context)

        if result.action in {"approve", "reject"}:
            response = result.response_text or ""
            self.notifier.send_message(message.sender_id, f"Resposta registrada: {response}")
            return {"status": "ok"}

        self.notifier.send_message(message.sender_id, "Comando não reconhecido. Use 'parametros' ou 'gerar agenda mensal'.")
        return {"status": "ignored"}

    def run_monthly_generation(self, sender_id: str, context: dict) -> dict:
        correlation_id = uuid.uuid4().hex
        workspace_name = context.get("workspace_name", "default")
        campaign_name = context.get("campaign_name", "default")
        parameters = context.get("parameters", {})

        with get_session() as session:
            workspace = repositories.get_or_create_workspace(session, workspace_name)
            campaign = repositories.get_or_create_campaign(session, workspace.id, campaign_name, parameters)
            repositories.add_audit_log(
                session,
                correlation_id=correlation_id,
                event="monthly_generation_started",
                payload={"parameters": parameters},
                workspace_id=workspace.id,
                campaign_id=campaign.id,
            )

        state = WorkflowState(
            correlation_id=correlation_id,
            workspace_name=workspace_name,
            campaign_name=campaign_name,
            workspace_id=workspace.id,
            campaign_id=campaign.id,
            parameters=parameters,
        )

        state.research_items = self.research.run(state.__dict__)
        state.ideas = self.ideation.run(state.__dict__)
        state.calendar_items = self.scheduler.run(state.__dict__)
        state.scripts = self.script_writer.run(state.__dict__)
        state.storyboards = self.storyboard.run(state.__dict__)
        state.editor_guides = self.editor_guide.run(state.__dict__)

        acceptance = self._evaluate_acceptance(state)
        self.notifier.send_message(sender_id, acceptance)

        with get_session() as session:
            repositories.add_audit_log(
                session,
                correlation_id=correlation_id,
                event="monthly_generation_completed",
                payload={"calendar_items": len(state.calendar_items)},
                workspace_id=workspace.id,
                campaign_id=campaign.id,
            )

        return {
            "status": "completed",
            "calendar_items": len(state.calendar_items),
            "scripts": len(state.scripts),
            "storyboards": len(state.storyboards),
        }

    def run_daily_review(self, sender_id: str, context: dict) -> dict:
        correlation_id = uuid.uuid4().hex
        workspace_name = context.get("workspace_name", "default")
        campaign_name = context.get("campaign_name", "default")
        parameters = context.get("parameters", {})
        with get_session() as session:
            workspace = repositories.get_or_create_workspace(session, workspace_name)
            campaign = repositories.get_or_create_campaign(session, workspace.id, campaign_name, parameters)
            repositories.add_audit_log(
                session,
                correlation_id=correlation_id,
                event="daily_review_started",
                payload={},
                workspace_id=workspace.id,
                campaign_id=campaign.id,
            )

        state = WorkflowState(
            correlation_id=correlation_id,
            workspace_name=workspace_name,
            campaign_name=campaign_name,
            workspace_id=workspace.id,
            campaign_id=campaign.id,
            parameters=parameters,
        )
        memory = self.memory.retrieve_recent(workspace.id)
        state.research_items = memory.get("research_items", [])
        state.ideas = memory.get("ideas", [])
        state.daily_review_notes = self.daily_review.run(state.__dict__)

        self.notifier.send_message(
            sender_id,
            "Revisão diária:\n" + "\n".join(state.daily_review_notes),
        )

        with get_session() as session:
            repositories.add_audit_log(
                session,
                correlation_id=correlation_id,
                event="daily_review_completed",
                payload={"notes": state.daily_review_notes},
                workspace_id=workspace.id,
                campaign_id=campaign.id,
            )
        return {"status": "completed", "notes": state.daily_review_notes}

    def _evaluate_acceptance(self, state: WorkflowState) -> str:
        checklist = [
            f"Itens de calendário: {len(state.calendar_items)}",
            f"Roteiros gerados: {len(state.scripts)}",
            f"Storyboards gerados: {len(state.storyboards)}",
            "Probabilidade de monetização é heurística e não garante ganhos.",
        ]
        return "Checklist de aceite:\n" + "\n".join(checklist) + "\nAprovar?"
