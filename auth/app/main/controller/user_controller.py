import logging
from flask import request
from flask_restplus import Resource
from app.main.service.auth_helper import Auth
from common.data_util import get_data, build_json_result

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, delete_account_by_id
from..worker.tasks import add as task_add
from common.log_utils import tcp_log
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
api = UserDto.api
_user = UserDto.user

parser = api.parser()


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    def get(self):
        """List all registered users"""
        LOG.error('=================---------------------- getting all user..')
        LOG.warning('=================---------------------- getting all user..')
        return build_json_result(get_all_users())

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        LOG.info('=================---------------------- creating user..')
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user', parser=parser)
    def get(self, public_id):
        """get a user given its identifier"""
        LOG.error('=================---------------------- get a user..1')
        LOG.info(request.headers)
        user = get_a_user(public_id)
        if not user:
            api.abort(404, message='Nie znaleziono użytkownika')
        else:
            return build_json_result(user)
    @api.doc('delete a user')
    def delete(self, public_id):
        """get a user given its identifier"""
        LOG.error('=================---------------------- get a user..')
        LOG.info(request.headers)
        return delete_account_by_id(public_id)

@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        post_data = request.get_json(force=True)
        owner_from = request.headers.get('X-Sub')
        return Auth.logout_user(auth_header, owner_from, get_data(post_data, 'device_id'))