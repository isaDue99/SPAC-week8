# SPAC-week8
Frontend for week 8 assignment, building on backend created during week 6-7 assignment.

### to run server + database in docker
From top directory: 'docker compose up'
If need to rebuild, open docker desktop and delete containers, images, volumes

### to run and use frontend (flask)
From top directory: 'flask --app front/main run', then navigate to http://127.0.0.1:5000 or whatever it says in the terminal
For debug: 'flask --app front/main run --debug'

### to run tests
From top directory: 'python -m unittest' to run all tests in /tests/-folder
Tests assume a MySQL server is already running, update tests/config.py to set log-on credentials