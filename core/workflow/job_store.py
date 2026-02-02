from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class JobStatus:
    job_id: str
    status: str
    result: dict = field(default_factory=dict)


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, JobStatus] = {}

    def create(self) -> JobStatus:
        job_id = str(uuid.uuid4())
        status = JobStatus(job_id=job_id, status="running")
        self._jobs[job_id] = status
        return status

    def set_result(self, job_id: str, result: dict) -> None:
        if job_id in self._jobs:
            self._jobs[job_id].status = "completed"
            self._jobs[job_id].result = result

    def get(self, job_id: str) -> JobStatus | None:
        return self._jobs.get(job_id)
