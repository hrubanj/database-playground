from __future__ import annotations

import csv
import tempfile

import duckdb

from data_generator.database.database_interface import Database


class DuckDBDatabase(Database):
    def __init__(self, database_file: str) -> None:
        self._database_file = database_file
        self._database: None | duckdb.DuckDBPyConnection = None

    async def connect(self) -> None:
        self._database = duckdb.connect(self._database_file)

    async def disconnect(self) -> None:
        self._database.close()
        self._database = None

    async def upload_to_table(
        self, table_name: str, data: list[tuple], columns: list[str]
    ) -> None:
        with tempfile.TemporaryFile() as tmp:
            dict_writer = csv.DictWriter(tmp, fieldnames=columns)
            dict_writer.writeheader()
            dict_writer.writerows([dict(zip(columns, row)) for row in data])
            self._database.execute(f"INSERT INTO {table_name} SELECT * FROM {tmp}")
