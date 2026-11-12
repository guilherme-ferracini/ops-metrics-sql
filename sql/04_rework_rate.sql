-- Rework: requests that went back to work after review, and the hours they cost
SELECT
    team,
    COUNT(*)                                        AS requests,
    SUM(reopened)                                   AS reopened,
    ROUND(100.0 * SUM(reopened) / COUNT(*), 1)      AS rework_pct,
    ROUND(AVG(CASE WHEN reopened = 1 THEN (julianday(closed_at) - julianday(opened_at)) * 24 END)
        - AVG(CASE WHEN reopened = 0 THEN (julianday(closed_at) - julianday(opened_at)) * 24 END), 1)
                                                    AS extra_hours_when_reopened
FROM requests
GROUP BY team
ORDER BY rework_pct DESC;
