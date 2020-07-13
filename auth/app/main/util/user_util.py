import logging
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
def get_user_profile(account_id):
    import requests
    import json
    from flask import request
    try:
        # headers = {'Host': 'auth.com', 'Authorization':'Bearer '+token}
        url = "http://user-api:5000/api/v1/kuser/profiles/" + str(account_id)
        response = requests.get(url)
        LOG.info(response)
        if response.ok and 'data' in response.json():
            # data = json.loads(response.json)
            # LOG.info(response)
            return response.json()['data']
        return None
    except Exception as e:
        LOG.info(e)
        return None