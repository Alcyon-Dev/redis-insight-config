help:
  @just -f {{justfile()}} --list

build:
  docker build -t alcyondev/redis-insight-config .

tag version:
  docker tag alcyondev/redis-insight-config alcyondev/redis-insight-config:{{version}}
  docker tag alcyondev/redis-insight-config alcyondev/redis-insight-config:latest

push version:
  docker push alcyondev/redis-insight-config:{{version}}
  docker push alcyondev/redis-insight-config:latest