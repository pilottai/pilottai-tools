import redis

from pilottai_tools.memory.redis.config import RedisConfig
from pilottai_tools.utils.logger import Logger

logger = Logger("RedisClient")


def get_redis_client():
    try:
        pool = redis.ConnectionPool(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            db=RedisConfig.REDIS_DB,
            password=RedisConfig.REDIS_PASSWORD,
            ssl=RedisConfig.REDIS_SSL,
            decode_responses=True,
            max_connections=10,
        )
        client = redis.Redis(connection_pool=pool)
        client.ping()  # Test connection
        logger.info(f"Connected to Redis at {RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}")
        return client
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        raise
