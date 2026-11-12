-- SLA compliance by team: share of requests closed within their SLA
SELECT
    team,
    COUNT(*)                                                         AS requests,
    ROUND(AVG((julianday(closed_at) - julianday(opened_at)) * 24), 1) AS avg_hours,
    SUM(CASE WHEN (julianday(closed_at) - julianday(opened_at)) * 24 > sla_hours THEN 1 ELSE 0 END) AS breached,
    ROUND(100.0 * SUM(CASE WHEN (julianday(closed_at) - julianday(opened_at)) * 24 <= sla_hours THEN 1 ELSE 0 END)
          / COUNT(*), 1)                                             AS sla_met_pct
FROM requests
GROUP BY team
ORDER BY sla_met_pct;
