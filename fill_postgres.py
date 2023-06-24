import asyncio

from constants import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from data_generator.database.postgres_database import PostgresDatabase
from fill_db import fill_database


async def main() -> None:
    database = PostgresDatabase(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    await fill_database(database)


if __name__ == "__main__":
    asyncio.run(main())
