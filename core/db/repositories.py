from __future__ import annotations

import datetime as dt
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.db import models


def get_or_create_workspace(session: Session, name: str) -> models.Workspace:
    workspace = session.execute(
        select(models.Workspace).where(models.Workspace.name == name)
    ).scalar_one_or_none()
    if workspace:
        return workspace
    workspace = models.Workspace(name=name)
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace


def get_or_create_campaign(
    session: Session, workspace_id: int, name: str, parameters: dict
) -> models.Campaign:
    campaign = session.execute(
        select(models.Campaign).where(
            models.Campaign.workspace_id == workspace_id,
            models.Campaign.name == name,
        )
    ).scalar_one_or_none()
    if campaign:
        campaign.parameters = parameters
        session.commit()
        session.refresh(campaign)
        return campaign
    campaign = models.Campaign(
        workspace_id=workspace_id,
        name=name,
        parameters=parameters,
    )
    session.add(campaign)
    session.commit()
    session.refresh(campaign)
    return campaign


def save_research_items(
    session: Session, workspace_id: int, campaign_id: int | None, items: Iterable[dict]
) -> list[models.ResearchItem]:
    records: list[models.ResearchItem] = []
    for item in items:
        record = models.ResearchItem(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            title=item["title"],
            summary=item["summary"],
            source_url=item["source_url"],
            tags=item.get("tags", []),
        )
        session.add(record)
        records.append(record)
    session.commit()
    return records


def save_ideas(
    session: Session, workspace_id: int, campaign_id: int | None, ideas: Iterable[dict]
) -> list[models.Idea]:
    records: list[models.Idea] = []
    for idea in ideas:
        record = models.Idea(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            title=idea["title"],
            description=idea["description"],
            monetization_score=idea["monetization_score"],
            justification=idea["justification"],
            confidence=idea["confidence"],
            tags=idea.get("tags", []),
        )
        session.add(record)
        records.append(record)
    session.commit()
    return records


def save_calendar_items(
    session: Session, workspace_id: int, campaign_id: int | None, items: Iterable[dict]
) -> list[models.CalendarItem]:
    records: list[models.CalendarItem] = []
    for item in items:
        record = models.CalendarItem(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            date=item["date"],
            title=item["title"],
            format=item["format"],
            status=item.get("status", "planned"),
            monetization_score=item["monetization_score"],
            justification=item["justification"],
            research_sources=item.get("research_sources", []),
        )
        session.add(record)
        records.append(record)
    session.commit()
    return records


def save_scripts(
    session: Session, workspace_id: int, campaign_id: int | None, scripts: Iterable[dict]
) -> list[models.Script]:
    records: list[models.Script] = []
    for script in scripts:
        record = models.Script(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            calendar_item_id=script.get("calendar_item_id"),
            script_type=script["script_type"],
            content=script["content"],
        )
        session.add(record)
        records.append(record)
    session.commit()
    return records


def save_storyboards(
    session: Session,
    workspace_id: int,
    campaign_id: int | None,
    storyboards: Iterable[dict],
) -> list[models.Storyboard]:
    records: list[models.Storyboard] = []
    for storyboard in storyboards:
        record = models.Storyboard(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            calendar_item_id=storyboard.get("calendar_item_id"),
            frames=storyboard["frames"],
        )
        session.add(record)
        records.append(record)
    session.commit()
    return records


def add_audit_log(
    session: Session,
    correlation_id: str,
    event: str,
    payload: dict,
    workspace_id: int | None = None,
    campaign_id: int | None = None,
) -> models.AuditLog:
    record = models.AuditLog(
        workspace_id=workspace_id,
        campaign_id=campaign_id,
        correlation_id=correlation_id,
        event=event,
        payload=payload,
    )
    session.add(record)
    session.commit()
    return record


def record_prompt_cache(
    session: Session,
    prompt_hash: str,
    provider: str,
    metadata: dict,
    workspace_id: int | None = None,
) -> models.PromptCacheMetadata:
    record = session.execute(
        select(models.PromptCacheMetadata).where(
            models.PromptCacheMetadata.prompt_hash == prompt_hash
        )
    ).scalar_one_or_none()
    if record:
        record.hit_count += 1
        record.last_used_at = dt.datetime.utcnow()
        record.metadata = metadata
        session.commit()
        session.refresh(record)
        return record
    record = models.PromptCacheMetadata(
        workspace_id=workspace_id,
        prompt_hash=prompt_hash,
        provider=provider,
        metadata=metadata,
        hit_count=1,
        last_used_at=dt.datetime.utcnow(),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
