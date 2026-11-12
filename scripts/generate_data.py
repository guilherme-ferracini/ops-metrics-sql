"""Generates a fictional event log for an accounting firm's operations desk.
Deterministic (fixed seed), so the committed CSVs and the tests always agree."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path(__file__).parents[1] / "data"
random.seed(42)

TEAMS = {"Payroll": ["vacation_calc", "termination", "admission"],
         "Tax": ["invoice_review", "tax_assessment"],
         "Accounting": ["bank_reconciliation", "statement_analysis"]}
SLA_HOURS = {"vacation_calc": 24, "termination": 48, "admission": 48, "invoice_review": 24,
             "tax_assessment": 72, "bank_reconciliation": 72, "statement_analysis": 96}
STAGES = ["intake", "in_progress", "review", "done"]
# typical hours per stage (mean); review is the deliberate bottleneck for Tax
STAGE_HOURS = {"Payroll": [2, 10, 6], "Tax": [3, 14, 30], "Accounting": [4, 30, 10]}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    start = datetime(2026, 9, 1, 8, 0)
    requests, events = [], []
    for i in range(1, 601):
        team = random.choice(list(TEAMS))
        rtype = random.choice(TEAMS[team])
        opened = start + timedelta(hours=random.randint(0, 24 * 85))
        t = opened
        reopened = random.random() < (0.12 if team == "Tax" else 0.05)
        for stage, mean in zip(STAGES[:-1], STAGE_HOURS[team]):
            dur = max(0.5, random.expovariate(1 / mean))
            events.append([i, stage, t.isoformat(" ", "minutes"), (t + timedelta(hours=dur)).isoformat(" ", "minutes")])
            t += timedelta(hours=dur)
        if reopened:  # one extra round of work and review
            for stage in ("in_progress", "review"):
                dur = max(0.5, random.expovariate(1 / 6))
                events.append([i, stage, t.isoformat(" ", "minutes"), (t + timedelta(hours=dur)).isoformat(" ", "minutes")])
                t += timedelta(hours=dur)
        requests.append([i, team, rtype, opened.isoformat(" ", "minutes"), t.isoformat(" ", "minutes"),
                         SLA_HOURS[rtype], int(reopened)])

    with (OUT / "requests.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["request_id", "team", "request_type", "opened_at", "closed_at", "sla_hours", "reopened"])
        w.writerows(requests)
    with (OUT / "stage_events.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["request_id", "stage", "entered_at", "left_at"])
        w.writerows(events)
    print(f"{len(requests)} requests, {len(events)} stage events -> {OUT}")


if __name__ == "__main__":
    main()
