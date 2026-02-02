from core.agents.intake import IntakeAgent
from core.workflow.messages import IncomingMessage


def test_intake_extracts_parameters() -> None:
    agent = IntakeAgent()
    message = IncomingMessage(sender_id="user", text="canal infantil shorts 2 shorts/dia pt-br")
    result = agent.run(message, context={})
    assert result.parameters["channel_type"] == "infantil"
    assert result.parameters["content_type"] == "shorts"
    assert result.parameters["frequency"] == "2 por dia"
    assert result.parameters["language"] == "pt-BR"
