from __future__ import annotations

import asyncio
import logging
import sys
from typing import Iterable, TypeVar

from data_generator.database.database_interface import Database
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


async def fill_table(database: Database, table: DataGenerator, max_id: int) -> None:
    logger.info("Processing: %s", table)
    table_name = table.get_table_name()
    await database.truncate_table(table_name)
    for batch_index, batch in enumerate(create_batches(table, max_id)):
        await database.upload_to_table(
            table_name=table_name,
            data=[tuple(obj.dict().values()) for obj in batch],
            columns=list(table.__fields__.keys()),
        )


async def fill_database(database: Database) -> None:
    await database.connect()
    objects = [
        [User, MAX_USER_ID],
        [Visit, MAX_VISIT_ID],
        [Post, MAX_POST_ID],
        [Comment, MAX_COMMENT_ID],
    ]
    try:
        tasks = [
            asyncio.create_task(fill_table(database, table, max_id))
            for table, max_id in objects
        ]
        await asyncio.gather(*tasks)
    finally:
        await database.disconnect()
