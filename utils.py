import json
import logging
from URLShortener.redis import redis_client

logger = logging.getLogger(__name__)


def set_url_details_redis(original_url, short_url, url_id):
    try:
        original_url_details = {"id": url_id, "original_url": original_url}
        redis_client.set(short_url, json.dumps(original_url_details))
    except Exception as e:
        logger.warning(f"Error during SET url related to short_url={short_url} to redis. the error is {e}")


def get_url_details_redis(short_url):
    original_url = None
    original_url_id = None
    try:
        original_url_details_redis = redis_client.get(short_url)
        if original_url_details_redis:
            original_url_details_redis = json.loads(original_url_details_redis)
            original_url = original_url_details_redis["original_url"]
            original_url_id = original_url_details_redis["id"]
    except Exception as e:
        logger.warning(f"Error during GET url related to short_url={short_url} to redis. the error is {e}")

    return original_url, original_url_id


def delete_url_details_redis(short_url):
    try:
        redis_client.delete(short_url)
    except Exception as e:
        logger.warning(f"Error during delete url related to short_url={short_url} to redis. the error is {e}")
