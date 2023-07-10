import redis

def init_redis_client() -> redis.Redis:
    redis_client = redis.Redis(
        host='redis',
        port=6379,
        decode_responses=True,
    )
    return redis_client

