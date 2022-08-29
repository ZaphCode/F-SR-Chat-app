from redis import Redis
from redis_om.connections import get_redis_connection
import config

def get_db() -> Redis:

    redis_db: Redis = None

    if config.node_env == "production":
        print("production database")
        redis_db = get_redis_connection(
            url = config.redis_db_url,
            password = config.redis_db_password,
            decode_responses = True
        )
    elif config.node_env == "development":
        print("development database")
        redis_db = get_redis_connection(
            url = "redis://localhost:6300",
            password = "dev-db-password",
            decode_responses = True
        )

    return redis_db


