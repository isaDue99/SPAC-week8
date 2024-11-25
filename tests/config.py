# This file holds the settings related to our tests module


### DATABASE SETTINGS

# The tests module assumes that a connection can be established to a running MySQL server (perhaps locally hosted)
# with these account credentials. Please update this file before running the tests module!

# The 'database' setting will be the name of the test database created on the server.
# This database is dropped once tests are complete, so running the tests module leaves no trace on the server

db_config = dict(
    user = "root",
    password = "Velkommen24",
    host = "localhost", # "localhost" or other address, will connect to MySQL's default port
    database = "test_db"
)