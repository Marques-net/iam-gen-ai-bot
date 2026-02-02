from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowState:
    correlation_id: str
    workspace_name: str
    campaign_name: str
    workspace_id: int | None = None
    campaign_id: int | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    research_items: list[dict[str, Any]] = field(default_factory=list)
    ideas: list[dict[str, Any]] = field(default_factory=list)
    calendar_items: list[dict[str, Any]] = field(default_factory=list)
    scripts: list[dict[str, Any]] = field(default_factory=list)
    storyboards: list[dict[str, Any]] = field(default_factory=list)
    editor_guides: list[dict[str, Any]] = field(default_factory=list)
    pending_questions: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    daily_review_notes: list[str] = field(default_factory=list)
