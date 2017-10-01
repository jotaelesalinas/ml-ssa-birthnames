"""
Create state level table
"""

from yoyo import step

__depends__ = {}

step(
    "CREATE TABLE state_level ("
        "year INT NOT NULL,"
        "state CHAR(2) NOT NULL,"
        "name VARCHAR(20) NOT NULL,"
        "gender CHAR(1) NOT NULL,"
        "pos INT NOT NULL,"
        "count INT DEFAULT NULL,"
        "perc DOUBLE DEFAULT NULL"
    ")",
    "DROP TABLE IF EXISTS state_level",
)
step(
    "CREATE INDEX idx_state_year ON state_level (year)",
    "DROP INDEX IF EXISTS idx_state_year",
)
step(
    "CREATE INDEX idx_state_state ON state_level (state)",
    "DROP INDEX IF EXISTS idx_state_state",
)
step(
    "CREATE INDEX idx_state_name ON state_level (name)",
    "DROP INDEX IF EXISTS idx_state_name",
)
step(
    "CREATE INDEX idx_state_gender ON state_level (gender)",
    "DROP INDEX IF EXISTS idx_state_gender",
)
