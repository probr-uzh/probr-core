#!/bin/sh

echo "########### setting up data-containers..."

# Mongo Data-Only Container
docker run -d -v //data/db --name probr_mongodb_data cogniteev/echo

# Postgres Data-Only Container
docker run -d -v //var/lib/postgresql --name probr_postgres_data cogniteev/echo

echo "########### setting up containers..."

# Redis Container
docker run -d --name probr_redis_1 redis:2.8.19

# Postgres Container
docker run -d -e "POSTGRES_USER=probr" -e "POSTGRES_PASSWORD=probr" --volumes-from probr_postgres_data --name probr_postgres_1 postgres:9.5

# MongoDB Container
docker run -d --volumes-from probr_mongodb_data --name probr_mongodb_1 mongo:3.0.6

# InfluxDB Container
docker run -d --volumes-from probr_mongodb_data --name probr_influxdb_1 tutum/influxdb:latest

echo "########### running containers..."
docker start probr_redis_1 probr_postgres_1 probr_mongodb_1 probr_influxdb_1