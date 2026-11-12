-- Weekly demand vs. throughput: requests opened and closed per ISO week
WITH opened AS (
    SELECT strftime('%Y-W%W', opened_at) AS week, COUNT(*) AS opened FROM requests GROUP BY week
),
closed AS (
    SELECT strftime('%Y-W%W', closed_at) AS week, COUNT(*) AS closed FROM requests GROUP BY week
)
SELECT
    o.week,
    o.opened,
    COALESCE(c.closed, 0)                AS closed,
    o.opened - COALESCE(c.closed, 0)     AS net_backlog_change
FROM opened o
LEFT JOIN closed c USING (week)
ORDER BY o.week;
