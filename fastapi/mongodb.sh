#!/bin/sh

docker run -d --name mongodb -e MONGO_INITDB_ROOT_USERNAME=root   \
-e MONGO_INITDB_ROOT_PASSWORD=1234   \
-e MONGO_INITDB_DATABASE=test  \
-p 27017:27017 mongo:latest