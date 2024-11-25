# SPAC-week8
Frontend for week 8 assignment, building on backend created during week 6-7 assignment.

### to run server + database in docker
From top directory: 'docker compose up'
If need to rebuild, open docker desktop and delete containers, images, volumes

### to run and use frontend (flask)
From top directory: 'flask --app front/hello run', then navigate to (webpages)
For debug: 'flask --app front/hello run --debug'

### to run tests
From top directory: 'python -m unittest' to run all tests in /tests/-folder
Tests assume a MySQL server is already running, update tests/config.py to set log-on credentials