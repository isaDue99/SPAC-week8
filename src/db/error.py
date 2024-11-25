# Custom error wrappers around mysql-connectors stupid error codes.


class DbError(Exception):
    def __init__(self, message="A Database error occured.") -> None:
        self.message = message
        super().__init__(message)


class DuplicateEntryError(DbError):
    def __init__(self, message="An entry with the same values already exist.") -> None:
        super().__init__(message)


class UnknownColumnError(DbError):
    def __init__(self, message="Unknown column error.") -> None:
        super().__init__(message)


class SyntaxError(DbError):
    def __init__(self, message="Syntax error.") -> None:
        super().__init__(message)


class CantConnectError(DbError):
    def __init__(self, message="Can't connect to database.") -> None:
        super().__init__(message)


class IdNotPresentError(DbError):
    def __init__(self, message="The ID is not present in the database."):
        super().__init__(message)


# MySQL error codes
DUPLICATE_ENTRY_ERROR = 1062
SYNTAX_ERROR = 1064
UNKNOWN_COLUMN_ERROR = 1054
CANT_CONNECT_ERROR = 2002

ERROR_MAP = {
    DUPLICATE_ENTRY_ERROR: DuplicateEntryError(),
    SYNTAX_ERROR: SyntaxError(),
    UNKNOWN_COLUMN_ERROR: UnknownColumnError(),
    CANT_CONNECT_ERROR: CantConnectError(),
}
