from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request

from core.logging import configure_logging
from core.schemas import JobStatusResponse, MonthlyGenerationRequest
from core.workflow.job_store import JobStore
from core.workflow.messages import IncomingMessage
from core.workflow.supervisor import SupervisorAgent

configure_logging()

app = FastAPI(title="IAM Gen AI Bot")
job_store = JobStore()
supervisor = SupervisorAgent()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request) -> dict:
    payload = await request.json()
    sender_id = payload.get("sender_id")
    text = payload.get("text", "")
    if not sender_id:
        raise HTTPException(status_code=400, detail="sender_id is required")
    message = IncomingMessage(sender_id=sender_id, text=text)
    return supervisor.handle_message(message)


@app.post("/workspaces/{workspace}/campaigns/{campaign}/generate-monthly")
def generate_monthly(workspace: str, campaign: str, body: MonthlyGenerationRequest) -> dict:
    job = job_store.create()
    context = {
        "workspace_name": workspace,
        "campaign_name": campaign,
        "parameters": body.parameters,
    }
    result = supervisor.run_monthly_generation(sender_id="api", context=context)
    job_store.set_result(job.job_id, result)
    return {"job_id": job.job_id}


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str) -> JobStatusResponse:
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return JobStatusResponse(job_id=job.job_id, status=job.status, result=job.result)


@app.post("/admin/run-daily-review")
def run_daily_review() -> dict:
    context = {"workspace_name": "default", "campaign_name": "default", "parameters": {}}
    return supervisor.run_daily_review(sender_id="admin", context=context)
