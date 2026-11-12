# Ops Metrics in SQL

[![tests](https://github.com/guilherme-ferracini/ops-metrics-sql/actions/workflows/tests.yml/badge.svg)](https://github.com/guilherme-ferracini/ops-metrics-sql/actions)

Turns an operations **event log** into the metrics an operations manager needs: **SLA compliance, cycle time (median and p90), stage bottlenecks, rework and weekly backlog**. Everything is in plain SQL (SQLite), with a terminal report and an HTML dashboard. No dependencies beyond the Python standard library.

## Why this exists

Before automating a process, I measure it. The questions are always the same: where does the time go, which team misses its SLA, how much rework is there, and is the backlog growing? This repo answers them from a fictional event log of an accounting firm's operations desk: 600 requests and about 1,900 stage events across Payroll, Tax and Accounting.

## What the data shows

From [`samples/report.txt`](samples/report.txt):

| Team | SLA met | Biggest stage | Rework |
|---|---:|---|---:|
| Tax | **48.8%** | **review = 61% of cycle time** | 10.5% |
| Payroll | 88.6% | in progress = 55% | 5.2% |
| Accounting | 89.4% | in progress = 66% | 5.1% |

Tax misses its SLA on half its requests, and the cause is not the work itself: requests spend most of their time **waiting for review**, and Tax has twice the rework of the other teams. The fix to test first is review capacity and better checks before review, not more people doing the work.

## Queries

| File | Question it answers | SQL techniques |
|---|---|---|
| `sql/01_sla_by_team.sql` | Which team misses its SLA? | conditional aggregation |
| `sql/02_cycle_time_by_type.sql` | How long does each request type take (median, p90)? | window functions, ranking-based percentiles |
| `sql/03_stage_bottlenecks.sql` | Where does the time go? | join, CTE, share of total with `SUM() OVER` |
| `sql/04_rework_rate.sql` | How much rework, and what does it cost? | conditional averages |
| `sql/05_weekly_volume.sql` | Is the backlog growing? | date bucketing, `LEFT JOIN` of two aggregates |

## Quickstart

```bash
python -m opsmetrics                              # terminal report
python -m opsmetrics --html out/dashboard.html    # HTML dashboard
python scripts/generate_data.py                   # regenerate the fictional data (fixed seed)
python -m pytest -q
```

## Data model

```
requests(request_id, team, request_type, opened_at, closed_at, sla_hours, reopened)
stage_events(request_id, stage, entered_at, left_at)     -- intake → in_progress → review → done
```

The same queries run on PostgreSQL or BigQuery with small date-function changes (`julianday` → `EXTRACT(EPOCH ...)`, `PERCENTILE_CONT` for the percentiles).

## License

MIT
