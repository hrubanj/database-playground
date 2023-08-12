import asyncio

from constants import DUCKDB_FILE_PATH
from data_generator.database.duckdb_database import DuckDBDatabase
from fill_db import fill_database


async def main() -> None:
    database = DuckDBDatabase(database_file=DUCKDB_FILE_PATH)
    await fill_database(database)


if __name__ == "__main__":
    asyncio.run(main())
