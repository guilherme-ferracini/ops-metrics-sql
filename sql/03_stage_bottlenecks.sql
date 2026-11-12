-- Where does time go? Average hours per stage and share of total cycle time, by team
WITH stage_time AS (
    SELECT
        r.team,
        e.stage,
        SUM((julianday(e.left_at) - julianday(e.entered_at)) * 24) AS hours
    FROM stage_events e
    JOIN requests r USING (request_id)
    GROUP BY r.team, e.stage
)
SELECT
    team,
    stage,
    ROUND(hours / (SELECT COUNT(*) FROM requests r2 WHERE r2.team = s.team), 1)   AS avg_hours_per_request,
    ROUND(100.0 * hours / SUM(hours) OVER (PARTITION BY team), 1)                 AS share_of_cycle_pct
FROM stage_time s
ORDER BY team, share_of_cycle_pct DESC;
