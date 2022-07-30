from redis_om.connections import get_redis_connection
import config

redis_db = get_redis_connection(
    host=config.redis_db_host,
    port=config.redis_db_port,
    password=None,
    decode_responses=True
)