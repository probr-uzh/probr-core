#!/bin/sh

echo "########### setting up containers..."
docker run -d --name probr_redis_1 redis:2.8.19
docker run -d -e "POSTGRES_USER=probr" -e "POSTGRES_PASSWORD=probr" --name probr_postgres_1 postgres:9.5
docker run -d --name probr_mongodb_1 mongo:3.1.6

echo "########### running containers..."
docker start probr_redis_1 probr_postgres_1 probr_mongodb_1