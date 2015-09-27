docker build -t probr_core .
docker build -t nginx ./install/docker/nginx/

# Data Only Container
docker run -d -v //app/static -v //app/media --name probr_data cogniteev/echo

# Probr Core Django App
docker stop probr_core
docker rm probr_core
docker run -d --expose 8001 --name probr_core --volumes-from probr_data --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/run.sh

# Probr Core Celery Worker
docker stop probr_core_worker
docker rm probr_core_worker
docker run -d --volumes-from probr_data --name probr_core_worker --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/worker.sh

# Probr Core WebSocket
docker stop probr_core_ws
docker rm probr_core_ws
docker run -d --expose 8002 --volumes-from probr_data --name probr_core_ws --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/websocket.sh

# nginx reverse-proxy
docker stop nginx
docker rm nginx
docker run -d -p 80:80 --name nginx --volumes-from probr_data --link probr_core:probr_core --link probr_core_ws:probr_core_ws --link probr_analysis:probr_analysis nginx