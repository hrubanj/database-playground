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
        quoted_name = f'"{table_name}"'
        columns_string = ", ".join(f'"{column}"' for column in columns)
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, "w") as tmpfile:
                dict_writer = csv.DictWriter(tmpfile, fieldnames=columns)
                dict_writer.writeheader()
                dict_writer.writerows([dict(zip(columns, row)) for row in data])
                self._database.execute(
                    f"INSERT INTO {quoted_name} ({columns_string}) SELECT {columns_string} "
                    f"FROM read_csv_auto('{tmp.name}');"
                )

    async def truncate_table(self, table_name: str) -> None:
        table = f'"{table_name}"'
        self._database.execute(f"TRUNCATE TABLE {table}")
