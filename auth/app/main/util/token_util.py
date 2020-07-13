import secrets
import redis
from app.main.config import key, AuthConfig, REDIS_URL
import logging
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
def generate_rand_token():
    return secrets.token_urlsafe()


def save_token_to_black_list(token, user_id):
    try:
        LOG.info('save_token_to_black_list')
        LOG.info(token)
        if not user_id:
            user_id = -1
        LOG.info(user_id)
        client = redis.StrictRedis.from_url(REDIS_URL) 
        # client.set_response_callback('EXPIRE',callback)
        client.set(token, user_id)
        client.expire(token, AuthConfig.EXP_TIME*24*3600)
        return True
    except Exception as e:
        LOG.exception(e)
        return True