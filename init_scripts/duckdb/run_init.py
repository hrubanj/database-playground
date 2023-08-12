from pathlib import Path

import duckdb

from constants import DUCKDB_FILE_PATH

INIT_SCRIPT = (Path(__file__).parent / "1.sql").read_text()


def main() -> None:
    db = duckdb.connect(DUCKDB_FILE_PATH)
    try:
        db.execute(INIT_SCRIPT)
    finally:
        db.close()


if __name__ == "__main__":
    main()
