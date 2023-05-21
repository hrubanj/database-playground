from __future__ import annotations

import datetime

from faker import Faker
from pydantic import BaseModel

FAKER_SEED = 43
Faker.seed(FAKER_SEED)
faker_generator = Faker()


def make_timestamp() -> int:
    return faker_generator.date_time_between_dates(
        datetime_start=datetime.datetime(2020, 1, 1),
        datetime_end=datetime.datetime(2024, 12, 31),
        tzinfo=datetime.UTC,
    ).timestamp()


class User(BaseModel):
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


class Visit(BaseModel):
    user_id: int
    site_id: int
    timestamp: int
    article_id: int
    ip: str
    user_agent: str

    @classmethod
    def generate(cls) -> Visit:
        return cls.parse_obj(
            {
                "user_id": faker_generator.pyint(),
                "site_id": faker_generator.pyint(),
                "timestamp": make_timestamp(),
                "article_id": faker_generator.pyint(),
                "ip": faker_generator.ipv4_public(),
                "user_agent": faker_generator.user_agent(),
            }
        )


if __name__ == "__main__":
    print(User.generate())
    print(Visit.generate())
