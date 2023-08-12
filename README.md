# Database playground

A collection of scripts and configs to test query performance tuning and other database related stuff.

## Dataset

All data are completely made up (see data generation [script](./data_generator/generator.py)).
The database should be loosely similar to what you could see in a simple discussion forum website backend.

It includes following tables:
### Table: user
Represents user information.

| Column   | Type |
|----------|------|
| id (PK)* | int  |
| name     | text |
| address  | text |
| email    | text |

### Table: visit
Records user visits to sites and related details.

| Column     | Type      |
|------------|-----------|
| id (PK)*   | int       |
| user_id    | int       |
| site_id    | int       |
| timestamp  | timestamp |
| post_id    | int       |
| origin_url | text      |
| ip         | text      |
| user_agent | text      |

### Table: post
Stores post information created by users.

| Column       | Type      |
|--------------|-----------|
| id (PK)*     | int       |
| user_id      | int       |
| time_created | timestamp |
| time_updated | timestamp |
| title        | text      |
| content      | text      |

### Table: comment
Contains user comments on posts.

| Column          | Type      |
|-----------------|-----------|
| id (PK)*        | int       |
| user_id         | int       |
| post_id         | int       |
| time_created    | timestamp |
| time_updated    | timestamp |
| content         | text      |
| upvotes_count   | int       |
| downvotes_count | int       |

`(PK)*`: (intended) Primary Key, not all databases allow defining genuine primary keys.

The `Type` column is only approximate as the actual type depends on the database. e.g., in Postgres,
we will sometimes use `varchar(255)` instead of `text`.

The dataset is probably not fit for practicing data analytic skills. The data generation process
does not ensure that, e.g., two users cannot have the same e-mail address. Also, the content of
comments and posts is just a version of *lorem ipsum*.

## Running examples
### Common requirements
- Python 3.8+ (tested with Python 3.11, but should be compatible with Python 3.8+)
- Python libraries in the `requirements.txt` file

Ideally, run the Python script in a virtual environment.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Postgres
**Additional requirements:**
- Docker

**How to:**
Navigate to the root of the repository, i.e., `database-playground/`.

Create database:
```bash
docker compose -f compose_files/postgres.compose.yml up
```
This will run docker container, and create a database called `performance_testing` with user `postgres` and password `postgres`,
and make it available on port `5433` on your computer.

Database name, username, password, and port can be changed in the compose file. If you decide to change them, be sure
to update corresponding values in the [constants.py](constants.py) file used by the data generation script.

Additionally, it will create tables described in the previous section.
(See [init scripts](init_scripts/postgres/1.sql) to check what gets run on database creation).

Populate tables:
```bash
python fill_postgres.py
```
This command will take a while as it needs to generate data and write them to the database.

That's it! You can now connect to the database with the credentials above and start querying.
I recommend using either [DataGrip](https://www.jetbrains.com/datagrip/) (paid), or [DBeaver](https://dbeaver.io/) (free).

### DuckDB
**IN PROGRESS**

The DuckDB example is not completely ironed out yet.

However, you should be able to run it without major problems.

**Additional requirements:** None

**How to:**

Navigate to the root of the repository, i.e., `database-playground/`.

Create database:
```bash
python init_scripts/duckdb/run_init.py
```
Populate tables:
```bash
python fill_duckdb.py
```

Connect to the database:

Connecting to DuckDB is a bit tricky. I have encountered problems when using Python script for database creation
and data generation, as the Python driver version was not compatible with DataGrip's driver.

I recommend running queries via the Python script.


## Issues

If you stumble upon any problems running examples, have any questions, suggestions or ideas, please
[open an issue](https://github.com/hrubanj/database-playground/issues/new/choose) or, ideally,
[submit a pull request](https://github.com/hrubanj/database-playground/pulls).

I am also happy to hear any feedback!