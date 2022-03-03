# Postgres Flask Docker Project
Basic Python Flask app in Docker which accesses a postgresql database in an other docker container

## Usage
### Build & Run application
Build the Docker image manually by cloning the Git repo.
```
$ git clone <link>
$ cd <foldername>
$ docker-compose up
```
### Verify the running app
visit http://localhost:1234
```
 Sample Docker Flask App
```
Response should be html with the first row of a table in the postgresql database

visit http://localhost:1234/api/v1/all/events?id=10 

to receive json response of event with id 10

## Explaination
Short explainaition of both docker containers

### App
Flask app, using the python:3.8-slim-buster image and installing python packages listed in `requirements.txt`.

The sqlalchemy package connect to the postgresql database.

I production, the database username, password etc would be environment variables handled by Secrets

### Database
from the latest `postgres` image a container is started. 

The `initial_setup.sql` file is copied into the `/docker-entrypoint-initdb.d` folder to initialize the database on first start.

### Network
the two seperate docker containers get build and started via the `docker-compose.yml` file in root.

A network acts as a bridge between the containers.

Post 1234:1234 is exposed

