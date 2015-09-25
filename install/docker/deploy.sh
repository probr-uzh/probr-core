docker build -t probr_core .
docker build -t nginx ./install/docker/nginx-proxy/

docker stop probr_core_worker
docker rm probr_core_worker
docker run -d --name probr_core_worker --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/worker.sh

docker stop probr_core_ws
docker rm probr_core_ws
docker run -d --expose 8002 --name probr_core_ws --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/websocket.sh

docker stop probr_core
docker rm probr_core
docker run -d --expose 8001 --name probr_core --link probr_postgres_1:postgres --link probr_mongodb_1:mongodb --link probr_redis_1:redis probr_core sh install/docker/web/run.sh

docker stop nginx
docker rm nginx
docker run -d -p 80:80 --name nginx --volumes-from probr_core --link probr_core:probr_core --link probr_core_ws:probr_core_ws --link probr_analysis:probr_analysis nginx