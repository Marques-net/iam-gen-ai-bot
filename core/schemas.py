from __future__ import annotations

from pydantic import BaseModel


class MonthlyGenerationRequest(BaseModel):
    parameters: dict


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: dict
