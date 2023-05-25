from typing import Protocol


class Database(Protocol):
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def upload_to_table(
        self, table_name: str, data: list[tuple], columns: list[str]
    ) -> None:
        ...
