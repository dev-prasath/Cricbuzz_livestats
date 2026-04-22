select * from matches

WITH match_performance AS (
    SELECT 
        p.player_id,
        p.player_name,
        p.team_id,
        m.match_id,
        m.winner_team_id,

        COALESCE(pmp.runs, 0) AS runs,
        COALESCE(pmp.wickets, 0) AS wickets,
        COALESCE(pmp.strike_rate, 0) AS strike_rate,

        CASE 
            WHEN p.team_id = m.winner_team_id THEN 1
            ELSE 0
        END AS is_win

    FROM player_match_performance pmp
    JOIN players p ON p.player_id = pmp.player_id
    JOIN matches_v2 m ON m.match_id = pmp.match_id
),

aggregated AS (
    SELECT 
        player_name,

        COUNT(*) AS total_matches,

        SUM(is_win) AS matches_won,

        ROUND(AVG(runs), 2) AS avg_runs_overall,

        ROUND(
            AVG(CASE WHEN is_win = 1 THEN runs ELSE NULL END), 2
        ) AS avg_runs_in_wins,

        COUNT(CASE WHEN runs >= 50 THEN 1 END) AS total_fifties,

        COUNT(CASE WHEN is_win = 1 AND runs >= 50 THEN 1 END) 
            AS winning_fifties,

        ROUND(STDDEV(runs), 2) AS consistency

    FROM match_performance
    GROUP BY player_name
)

SELECT *
FROM aggregated
ORDER BY 
    matches_won DESC,
    avg_runs_overall DESC;


SELECT COUNT(*) FROM matches_v2 WHERE winner_team_id IS NOT NULL;
SELECT COUNT(*) FROM player_match_performance;
SELECT COUNT(*) 
FROM player_match_performance pmp
JOIN matches_v2 m ON pmp.match_id = m.match_id;



SELECT COUNT(*) 
FROM player_match_performance pmp
JOIN players p ON p.player_id = pmp.player_id
JOIN matches_v2 m ON m.match_id = pmp.match_id
WHERE p.team_id = m.winner_team_id;


WITH match_performance AS (
    SELECT 
        p.player_name,
        pmp.match_id,
        COALESCE(pmp.runs, 0) AS runs,
        COALESCE(pmp.wickets, 0) AS wickets,
        COALESCE(pmp.strike_rate, 0) AS strike_rate
    FROM player_match_performance pmp
    JOIN players p ON p.player_id = pmp.player_id
),

aggregated AS (
    SELECT 
        player_name,
        COUNT(*) AS total_matches,
        ROUND(AVG(runs), 2) AS avg_runs,
        ROUND(AVG(strike_rate), 2) AS avg_strike_rate,
        COUNT(CASE WHEN runs >= 50 THEN 1 END) AS fifties,
        COUNT(CASE WHEN wickets >= 3 THEN 1 END) AS good_bowling,
        ROUND(STDDEV(runs), 2) AS consistency
    FROM match_performance
    GROUP BY player_name
)

SELECT *
FROM aggregated
WHERE total_matches >= 2
ORDER BY avg_runs DESC;


WITH match_performance AS (
    SELECT 
        p.player_name,
        pmp.match_id,
        COALESCE(pmp.runs, 0) AS runs,
        COALESCE(pmp.wickets, 0) AS wickets,
        COALESCE(pmp.strike_rate, 0) AS strike_rate
    FROM player_match_performance pmp
    JOIN players p ON p.player_id = pmp.player_id
),

aggregated AS (
    SELECT 
        player_name,
        COUNT(*) AS total_matches,
        ROUND(AVG(runs), 2) AS avg_runs,
        ROUND(AVG(strike_rate), 2) AS avg_strike_rate,
        COUNT(CASE WHEN runs >= 50 THEN 1 END) AS fifties,
        COUNT(CASE WHEN wickets >= 3 THEN 1 END) AS good_bowling,
        ROUND(STDDEV(runs), 2) AS consistency
    FROM match_performance
    GROUP BY player_name
)

SELECT 
    player_name,
    total_matches,
    avg_runs,
    avg_strike_rate,
    fifties,
    good_bowling,
    consistency,
    ROUND(avg_runs + (good_bowling * 5), 2) AS impact_score
FROM aggregated
WHERE total_matches >= 2
ORDER BY impact_score DESC;



CREATE TABLE all_time_records (
    format TEXT,
    category TEXT,   -- Men / Women
    player_name TEXT,
    highest_score INTEGER
);


INSERT INTO all_time_records (format, category, player_name, highest_score)
VALUES
-- Men's records
('Test', 'Men', 'Brian Lara', 400),
('ODI', 'Men', 'Rohit Sharma', 264),
('T20', 'Men', 'Chris Gayle', 175),

-- Women's records
('Test', 'Women', 'Kiran Baluch', 242),
('ODI', 'Women', 'Belinda Clark', 229),
('T20', 'Women', 'Deandra Dottin', 112);



SELECT 
    r.format,
    r.category,
    r.player_name,
    r.highest_score AS all_time_score
FROM all_time_records r;


select * from venues

SELECT COUNT(*) FROM bowling_performance;




CREATE TABLE bowling_performance (
    id SERIAL PRIMARY KEY,
    match_id BIGINT,
    player_id BIGINT,
    player_name TEXT,
    overs FLOAT,
    runs_conceded INT,
    wickets INT,
    economy FLOAT
);
drop table bowling_performance

SELECT COUNT(*) FROM bowling_performance;

CREATE TABLE IF NOT EXISTS bowling_performance_v2 (
    id SERIAL PRIMARY KEY,
    match_id BIGINT,
    player_id BIGINT,
    player_name TEXT,
    overs FLOAT,
    runs INTEGER,
    wickets INTEGER,
    economy FLOAT
);

SELECT * FROM bowling_performance_v2;


SELECT 
    bp.player_name,

    COUNT(*) AS matches_played,

    ROUND(AVG(bp.economy)::numeric, 2) AS avg_economy,

    SUM(bp.wickets) AS total_wickets

FROM bowling_performance_v2 bp

WHERE bp.overs >= 4

GROUP BY bp.player_name

ORDER BY total_wickets DESC;


select * from player_match_performance

select * from matches where match_id=152302

ALTER TABLE player_match_performance
DROP COLUMN balls,
DROP COLUMN strike_rate,
DROP COLUMN team_id;

ALTER TABLE player_match_performance
ADD COLUMN team_id BIGINT;


select * from player_match_performance


DROP TABLE IF EXISTS player_match_performance;

CREATE TABLE player_match_performance_v2 (
    match_id BIGINT,
    player_id BIGINT,
    runs INT,
    team_id BIGINT,
    PRIMARY KEY (match_id, player_id)
);

select * from player_match_performance_v2


SELECT player_id, COUNT(*) 
FROM player_match_performance_v2
GROUP BY player_id
ORDER BY COUNT(*) DESC;


SELECT COUNT(*) FROM player_match_performance_v2;
SELECT COUNT(*)
FROM player_match_performance_v2 pmp
JOIN matches_v2 m ON pmp.match_id = m.match_id;

SELECT DISTINCT pmp.match_id
FROM player_match_performance_v2 pmp
WHERE pmp.match_id NOT IN (
    SELECT match_id FROM matches_v2
);


SELECT 
    player_id,
    COUNT(*) AS matches
FROM player_match_performance_v2
GROUP BY player_id
ORDER BY matches DESC;



WITH ranked_matches AS (
    SELECT 
        pmp.player_id,
        p.player_name,
        pmp.runs,
        m.start_date,

        ROW_NUMBER() OVER (
            PARTITION BY pmp.player_id
            ORDER BY m.start_date DESC
        ) AS rn

    FROM player_match_performance_v2 pmp

    JOIN matches_v2 m 
        ON pmp.match_id = m.match_id

    JOIN players p
        ON p.player_id = pmp.player_id

    WHERE pmp.runs IS NOT NULL
),

last_10 AS (
    SELECT *
    FROM ranked_matches
    WHERE rn <= 10
)

SELECT 
    player_name,

    COUNT(*) AS matches_considered,

    ROUND(AVG(runs)::numeric, 2) AS avg_runs_last_10,

    ROUND(AVG(CASE WHEN rn <= 5 THEN runs END)::numeric, 2) AS avg_runs_last_5,

    COUNT(CASE WHEN runs >= 50 THEN 1 END) AS fifties,

    ROUND(STDDEV(runs)::numeric, 2) AS consistency_score

FROM last_10

GROUP BY player_name

HAVING COUNT(*) >= 3   -- 🔥 important filter

ORDER BY avg_runs_last_10 DESC;