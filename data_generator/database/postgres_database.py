from __future__ import annotations

import asyncpg

from data_generator.database.database_interface import Database


class PostgresDatabase(Database):
    def __init__(
        self, user: str, password: str, database: str, host: str, port: int
    ) -> None:
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self._connection: asyncpg.Connection | None = None

    async def connect(self) -> None:
        self._connection = await asyncpg.connect(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
        )

    async def disconnect(self) -> None:
        await self._connection.close()
        self._connection = None

    async def upload_to_table(
        self, table_name: str, data: list[tuple], columns: list[str]
    ) -> None:
        await self._connection.copy_records_to_table(
            table_name=table_name, records=data
        )
