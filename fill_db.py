from __future__ import annotations

import asyncio
from typing import Iterable, TypeVar

from data_generator.database.database_interface import Database
from data_generator.database.postgres_database import PostgresDatabase
from data_generator.generator import (
    MAX_COMMENT_ID,
    MAX_POST_ID,
    MAX_USER_ID,
    MAX_VISIT_ID,
    Comment,
    DataGenerator,
    Post,
    User,
    Visit,
)

T = TypeVar("T", bound=DataGenerator)


def create_batches(
    data_type: T, total_count: int, batch_size: int = 1000
) -> Iterable[list[T]]:
    remaining_count = total_count
    while remaining_count > 0:
        batch_count = min(batch_size, remaining_count)
        remaining_count -= batch_count
        yield [data_type.generate() for _ in range(batch_count)]


async def fill_database(database: Database) -> None:
    await database.connect()
    objects = [
        [User, MAX_USER_ID],
        [Visit, MAX_VISIT_ID],
        [Post, MAX_POST_ID],
        [Comment, MAX_COMMENT_ID],
    ]
    for data_type, total_count in objects:
        for batch in create_batches(data_type, total_count):
            await database.upload_to_table(
                table_name=data_type.__name__.lower(),
                data=[tuple(obj.dict().values()) for obj in batch],
                columns=list(data_type.__fields__.keys()),
            )


async def main() -> None:
    database = PostgresDatabase(
        user="postgres",
        password="postgres",
        database="performancetesting",
        host="localhost",
        port=5433,
    )

    await fill_database(database)


if __name__ == "__main__":
    asyncio.run(main())
