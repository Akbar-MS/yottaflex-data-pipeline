import json
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path


def create_run_id():
    return str(uuid.uuid4())


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


def start_run():
    return {
        "run_id": create_run_id(),
        "start_time": utc_timestamp(),
        "start_epoch": time.time(),
        "status": "RUNNING"
    }


def finish_run(
    run,
    metrics,
    status="SUCCESS",
    error=None
):
    end_epoch = time.time()

    run["end_time"] = utc_timestamp()
    run["duration_seconds"] = round(
        end_epoch - run["start_epoch"], 3
    )
    run["status"] = status

    run.pop("start_epoch", None)

    run.update(metrics)

    if error:
        run["error"] = error

    return run


def save_run_report(run_report, reports_dir: Path):
    reports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = (
        reports_dir /
        f"run_{run_report['run_id']}.json"
    )

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(
            run_report,
            file,
            indent=4
        )

    return report_path