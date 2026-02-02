from __future__ import annotations

import time

from apscheduler.schedulers.background import BackgroundScheduler

from core.logging import configure_logging
from core.workflow.supervisor import SupervisorAgent

configure_logging()

scheduler = BackgroundScheduler()
supervisor = SupervisorAgent()


def run_daily_review() -> None:
    supervisor.run_daily_review(sender_id="worker", context={"workspace_name": "default", "campaign_name": "default", "parameters": {}})


def main() -> None:
    scheduler.add_job(run_daily_review, "interval", hours=24)
    scheduler.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
