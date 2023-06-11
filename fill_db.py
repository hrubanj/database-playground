from __future__ import annotations

import asyncio
import logging
import sys
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
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


def create_batches(
    data_type: T, total_count: int, batch_size: int = 10_000
) -> Iterable[list[T]]:
    current_count = 0
    while current_count < total_count:
        batch = []
        for _ in range(min(total_count - current_count, batch_size)):
            current_count += 1
            batch.append(data_type.generate(current_count))
        yield batch


async def fill_database(database: Database) -> None:
    await database.connect()
    objects = [
        [User, MAX_USER_ID],
        [Visit, MAX_VISIT_ID],
        [Post, MAX_POST_ID],
        [Comment, MAX_COMMENT_ID],
    ]
    for data_type, total_count in objects:
        logger.info("Processing: %s", data_type)
        table_name = data_type.get_table_name()
        await database.truncate_table(table_name)
        for batch_index, batch in enumerate(create_batches(data_type, total_count)):
            await database.upload_to_table(
                table_name=table_name,
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
