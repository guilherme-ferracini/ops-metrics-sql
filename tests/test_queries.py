from opsmetrics.run import load, run_all, to_html

CON = load()
RESULTS = run_all(CON)


def rows(stem):
    cols, data = RESULTS[stem]
    return [dict(zip(cols, r)) for r in data]


def test_every_query_returns_rows():
    assert len(RESULTS) == 5
    assert all(data for _, data in RESULTS.values())


def test_sla_counts_add_up():
    total = CON.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    sla = rows("01_sla_by_team")
    assert sum(r["requests"] for r in sla) == total
    assert all(0 <= r["sla_met_pct"] <= 100 for r in sla)


def test_median_not_above_p90():
    for r in rows("02_cycle_time_by_type"):
        assert r["median_hours"] <= r["p90_hours"]


def test_stage_shares_sum_to_100_per_team():
    shares = {}
    for r in rows("03_stage_bottlenecks"):
        shares[r["team"]] = shares.get(r["team"], 0) + r["share_of_cycle_pct"]
    assert all(abs(v - 100) < 0.5 for v in shares.values())


def test_review_is_the_tax_bottleneck():
    tax = [r for r in rows("03_stage_bottlenecks") if r["team"] == "Tax"]
    assert tax[0]["stage"] == "review"


def test_weekly_opened_matches_total():
    total = CON.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    assert sum(r["opened"] for r in rows("05_weekly_volume")) == total


def test_html_dashboard_renders():
    page = to_html(RESULTS, "Test")
    assert page.startswith("<!DOCTYPE html>") and "Sla by team" in page


def test_tax_has_the_worst_sla():
    assert rows("01_sla_by_team")[0]["team"] == "Tax"
