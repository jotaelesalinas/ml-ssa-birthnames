"""
Create views
"""

from yoyo import step

__depends__ = {}

step(
    "CREATE VIEW IF NOT EXISTS country_with_scores AS "
        "SELECT "
                "year, '_USA' as state, name, gender, count,"
                "(1001 - pos) / 10 as score,"
                "((1001 - pos) / 10 * (1001 - pos) / 10 * (1001 - pos) / 10 * (1001 - pos) / 10) / 1000000.0 as score2 "
            "FROM country_level",
    "DROP VIEW IF EXISTS country_with_scores",
)
step(
    "CREATE VIEW IF NOT EXISTS states_with_scores AS "
        "SELECT "
                "year, state, name, gender, count,"
                "(101 - pos) as score,"
                "((101 - pos) * (101 - pos) * (101 - pos) * (101 - pos)) / 1000000.0 as score2 "
            "FROM state_level",
    "DROP VIEW IF EXISTS states_with_scores",
)
step(
    "CREATE VIEW IF NOT EXISTS scores AS "
        "SELECT * FROM country_with_scores UNION ALL SELECT * FROM states_with_scores",
    "DROP VIEW IF EXISTS scores",
)
step(
    "CREATE VIEW IF NOT EXISTS top_100_per_year AS "
        "SELECT year, name, gender "
            "FROM country_level "
            "WHERE pos <= 100",
    "DROP VIEW IF EXISTS top_100_per_year",
)
