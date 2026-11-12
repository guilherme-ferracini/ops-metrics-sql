-- Cycle time per request type: median and p90 (SQLite has no PERCENTILE, so we rank rows)
WITH durations AS (
    SELECT
        request_type,
        (julianday(closed_at) - julianday(opened_at)) * 24 AS hours
    FROM requests
),
ranked AS (
    SELECT
        request_type,
        hours,
        ROW_NUMBER() OVER (PARTITION BY request_type ORDER BY hours) AS rn,
        COUNT(*)     OVER (PARTITION BY request_type)                AS n
    FROM durations
)
SELECT
    request_type,
    MAX(n)                                                                AS requests,
    ROUND(MAX(CASE WHEN rn = (n + 1) / 2 THEN hours END), 1)               AS median_hours,
    ROUND(MAX(CASE WHEN rn = CAST(0.9 * n AS INTEGER) THEN hours END), 1)  AS p90_hours
FROM ranked
GROUP BY request_type
ORDER BY median_hours DESC;
