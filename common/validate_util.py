from flask import request
import re
import logging
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
def check_owner_resource(owner_id):
    owner_from = request.headers.get('X-Sub')
    role = request.headers.get('X-Role')
    if role =='admin':
        return True
    if int(owner_from) == int(owner_id):
        return True
    else:
        return False

def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def validate_data(post_data, schema):
    from cerberus import Validator
    v = Validator(schema, purge_unknown=True)
    ok = v.validate(post_data)
    return ok, v.errors