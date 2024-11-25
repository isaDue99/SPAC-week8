import os
from .db_connection import DbConnection
import pathlib as path
import logging

LOG = logging.getLogger(__name__)


def _execute_sql_script(db_cursor, script_path: path.Path):
    """
    Executes each statement in SQL script.

    Thanks mysql-connector for not having a built-in execute script function.
    """

    # We have to go through the SQL script manually and seperate statements by the ';' character.
    with open(script_path, encoding="utf-8") as f:
        statement_buf = ""
        for line in f:
            # Skip comments
            if line.startswith("--"):
                continue

            for char in line:
                statement_buf += char

                if char == ";":
                    # Statement terminator. Execute the statement.
                    db_cursor.execute(statement_buf)
                    statement_buf = ""


def migrate_db(db: DbConnection, migration_script_dir: str):
    """
    Migrates db using the SQL scripts in the provided directory.
    """

    directory = path.Path(migration_script_dir).absolute()
    with db.get_cursor() as cur:
        try:
            # Iterate through all files in the directory
            for filename in sorted(os.listdir(directory)):
                if not filename.endswith(".sql"):
                    continue

                filepath = os.path.join(directory, filename)
                LOG.debug(f"Running migration script: {filename}")
                _execute_sql_script(cur, filepath)

        except Exception as e:
            LOG.error(f"Error while executing migration scripts: {e}")

    db.commit()
