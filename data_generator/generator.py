from __future__ import annotations

import datetime

from faker import Faker
from pydantic import BaseModel

MAX_USER_ID = 10_000
MAX_POST_ID = 1_000_000
MAX_VISIT_ID = 1_000_000
MAX_COMMENT_ID = 1_000_000
MIN_DATETIME = datetime.datetime(2010, 1, 1, 0, 0, 0)
MAX_DATETIME = datetime.datetime(2024, 1, 1, 0, 0, 0)

FAKER_SEED = 43

Faker.seed(FAKER_SEED)
faker_generator = Faker()


def post_datetime_from_id(item_id: int) -> datetime.datetime:
    return MIN_DATETIME + datetime.timedelta(
        seconds=item_id * (MAX_DATETIME - MIN_DATETIME).total_seconds() / MAX_POST_ID
    )


class DataGenerator(BaseModel):
    @classmethod
    def generate(cls, item_id: int) -> DataGenerator:
        raise NotImplementedError

    @classmethod
    def get_table_name(cls) -> str:
        return str(cls.__name__.lower())


class User(DataGenerator):
    name: str
    address: str
    email: str
    id: int

    @classmethod
    def generate(cls, item_id: int) -> User:
        return cls.parse_obj(
            {
                "name": faker_generator.name(),
                "address": faker_generator.address(),
                "email": faker_generator.email(),
                "id": item_id,
            }
        )


class Visit(DataGenerator):
    user_id: int
    site_id: int
    timestamp: datetime.datetime
    post_id: int
    origin_url: str
    ip: str
    user_agent: str
    id: int

    @classmethod
    def generate(cls, item_id: int) -> Visit:
        post_id = faker_generator.pyint(max_value=MAX_POST_ID)
        min_timestamp = post_datetime_from_id(post_id)
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(max_value=MAX_USER_ID),
                "site_id": faker_generator.pyint(max_value=3),
                "timestamp": faker_generator.date_time_between(
                    min_timestamp, MAX_DATETIME
                ),
                "post_id": post_id,
                "origin_url": faker_generator.url(),
                "ip": faker_generator.ipv4_public(),
                "user_agent": faker_generator.user_agent(),
                "id": item_id,
            }
        )


class Post(DataGenerator):
    user_id: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
    title: str
    content: str
    id: int

    @classmethod
    def generate(cls, item_id: int) -> Post:
        created = post_datetime_from_id(item_id)
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(max_value=MAX_USER_ID),
                "time_created": created,
                "time_updated": faker_generator.date_time_between(
                    created, MAX_DATETIME
                ),
                "title": faker_generator.text(),
                "content": faker_generator.text(),
                "id": item_id,
            }
        )


class Comment(DataGenerator):
    user_id: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
    post_id: int
    content: str
    upvotes_count: int
    downvotes_count: int
    id: int

    @classmethod
    def generate(cls, item_id: int) -> Comment:
        post_id = faker_generator.pyint(max_value=MAX_POST_ID)
        min_created = post_datetime_from_id(post_id)
        created = faker_generator.date_time_between(min_created, MAX_DATETIME)
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(max_value=MAX_USER_ID),
                "time_created": created,
                "time_updated": faker_generator.date_time_between(
                    created, MAX_DATETIME
                ),
                "post_id": post_id,
                "content": faker_generator.text(),
                "upvotes_count": faker_generator.pyint(),
                "downvotes_count": faker_generator.pyint(),
                "id": item_id,
            }
        )
