from pathlib import Path

DUCKDB_FILE_PATH = (Path(__file__).parent / "duckdbdata.db").resolve().as_posix()

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "performancetesting"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5433
