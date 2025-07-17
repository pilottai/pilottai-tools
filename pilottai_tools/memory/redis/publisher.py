import logging
import json
from redis.client import get_redis_client

logger = logging.getLogger(__name__)
client = get_redis_client()

def publish_to_redis(channel: str, data: dict):
    try:
        message = json.dumps(data)
        client.publish(channel, message)
        logger.info(f"Published to Redis channel '{channel}': {message}")
    except Exception as e:
        logger.error(f"Failed to publish to Redis: {e}")
