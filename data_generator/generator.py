from __future__ import annotations

import datetime

from faker import Faker
from pydantic import BaseModel

MAX_USER_ID = 100_000
MAX_POST_ID = 10_000_000
MAX_VISIT_ID = 10_000_000
MAX_COMMENT_ID = 10_000_000
FAKER_SEED = 43
Faker.seed(FAKER_SEED)
faker_generator = Faker()


class DataGenerator(BaseModel):
    @classmethod
    def generate(cls) -> DataGenerator:
        raise NotImplementedError


class User(DataGenerator):
    name: str
    address: str
    email: str

    @classmethod
    def generate(cls) -> User:
        return cls.parse_obj(
            {
                "name": faker_generator.name(),
                "address": faker_generator.address(),
                "email": faker_generator.email(),
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

    @classmethod
    def generate(cls) -> Visit:
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(max_value=MAX_USER_ID),
                "site_id": faker_generator.pyint(max_value=3),
                "timestamp": faker_generator.date_time(),
                "post_id": faker_generator.pyint(max_value=MAX_POST_ID),
                "origin_url": faker_generator.url(),
                "ip": faker_generator.ipv4_public(),
                "user_agent": faker_generator.user_agent(),
            }
        )


class Post(DataGenerator):
    user_id: int
    time_created: datetime.datetime
    time_updated: datetime.datetime
    post_id: int
    title: str
    content: str

    @classmethod
    def generate(cls) -> Post:
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(max_value=MAX_USER_ID),
                "time_created": faker_generator.date_time(),
                "time_updated": faker_generator.date_time(),
                "post_id": faker_generator.pyint(max_value=MAX_POST_ID),
                "title": faker_generator.text(),
                "content": faker_generator.text(),
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

    @classmethod
    def generate(cls) -> Comment:
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(),
                "time_created": faker_generator.date_time(),
                "time_updated": faker_generator.date_time(),
                "post_id": faker_generator.pyint(),
                "content": faker_generator.text(),
                "upvotes_count": faker_generator.pyint(),
                "downvotes_count": faker_generator.pyint(),
            }
        )


if __name__ == "__main__":
    print(User.generate())
    print(Visit.generate())
    print(Post.generate())
