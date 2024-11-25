import mysql.connector as sql
from typing import Any, Self
from .error import ERROR_MAP
from mysql.connector.errors import Error


class DbMySQLCursor:
    """
    A wrapper around an internal cursor.

    Primarily serves the purpose of wrapping mysql errors with something more useful.
    """

    def __init__(self, wrapper_cursor: sql.connection.MySQLCursor) -> None:
        self._cursor = wrapper_cursor
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self._cursor.__exit__(exc_type, exc_value, traceback)

    def execute(self, operation: str, params: tuple[Any] = None, multi: bool = False):
        """
        Wrapper around MySQLCursor.execute()
        """

        try:
            self._cursor.execute(operation, params, multi)
        except Error as err:
            err_code = err.errno
            raise ERROR_MAP[err_code]

    def fetchall(self) -> list[sql.connection.RowType]:
        return self._cursor.fetchall()

    def fetchone(self) -> sql.connection.RowType | None:
        return self._cursor.fetchone()
