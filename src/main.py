# main script to interact with a product management system
import os
from waitress import serve
from .db.db_connection import DbConnection
from .db.migrate import migrate_db
from .webserver.api import api

DEBUG_SERVER = False


def main():
    is_docker = os.environ.get("DOCKER", False)

    if is_docker:
        backend_host = os.environ["BACKEND_HOST"]
        backend_port = os.environ["BACKEND_PORT"]
        db_user = os.environ["DB_USER"]
        db_password = os.environ["DB_PASSWORD"]
        db_host = os.environ["DB_HOST"]
        db_port = os.environ["DB_PORT"]
    else:
        print("Not running in Docker environment")
        backend_host = "localhost"
        backend_port = 8080
        db_user = "root"
        db_password = "root"
        db_host = "localhost"
        db_port = 3306

    # Setup the DB singleton
    db = DbConnection(db_user, db_password, db_host, db_port, "lager")
    migrate_db(db, "migrations/")

    if DEBUG_SERVER:
        api.run(host=backend_host, port=backend_port)
    else:
        serve(api, host=backend_host, port=backend_port)


if __name__ == "__main__":
    main()
