from contextlib import closing
from functools import wraps
from pathlib import Path
from sqlite3 import connect

import pandas as pd


db_path = Path(__file__).resolve().parent / "employee_events.db"


class QueryMixin:
    def pandas_query(self, sql_query):
        with closing(connect(db_path)) as connection:
            return pd.read_sql_query(sql_query, connection)

    def query(self, sql_query):
        with closing(connect(db_path)) as connection:
            with closing(connection.cursor()) as cursor:
                return cursor.execute(sql_query).fetchall()


def query(func):
    """Run a method that returns SQL and return its rows as tuples."""

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        return QueryMixin().query(query_string)

    return run_query
