`redis-insight-config` (not affiliated with Redis or Redis Insight) is a short-lived helper container to preconfigure Redis Insight.

With `redis-insight-config`, your Redis Insight instance will always be preconfigured with a connection to your dockerized Redis instance.

You can also pre-accept Redis Insight's EULA and privacy policy, but please only do so after reading and understanding the official documents.

In your `docker-compose.yaml`:
```yaml
services:
    redis:
        image: redis:latest
        ports:
            - 6379:6379

    redis-insight:
        image: redis/redisinsight:latest
        depends_on:
            - redis
        ports:
            - 5540:5540

    redis-insight-config:
        image: alcyondev/redis-insight-config:latest
        environment:
            RI_ACCEPT_EULA: true
            #RI_BASE_URL: "http://redis-insight:5540"
            #RI_CONNECTION_NAME: "Docker (redis)"
            #REDIS_HOST: "redis"
            #REDIS_PORT: 6379
        depends_on:
            - redis
            - redis-insight
```
