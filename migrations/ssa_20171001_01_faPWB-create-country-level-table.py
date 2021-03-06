"""
Create country level table
"""

from yoyo import step

__depends__ = {}

step(
    "CREATE TABLE IF NOT EXISTS country_level ("
        "year INT NOT NULL,"
        "name VARCHAR(32) NOT NULL,"
        "gender CHAR(1) NOT NULL,"
        "pos INT NOT NULL,"
        "count INT DEFAULT NULL,"
        "perc DOUBLE DEFAULT NULL,"
        "PRIMARY KEY (year, name, gender)"
    ")",
    "DROP TABLE IF EXISTS country_level",
)
step(
    "CREATE INDEX IF NOT EXISTS idx_country_year ON country_level (year)",
    "DROP INDEX IF EXISTS idx_country_year",
)
step(
    "CREATE INDEX IF NOT EXISTS idx_country_name ON country_level (name)",
    "DROP INDEX IF EXISTS idx_country_name",
)
step(
    "CREATE INDEX IF NOT EXISTS idx_country_gender ON country_level (gender)",
    "DROP INDEX IF EXISTS idx_country_gender",
)
