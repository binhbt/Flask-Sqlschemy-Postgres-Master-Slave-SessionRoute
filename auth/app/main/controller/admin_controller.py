import logging
from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_email
from..worker.tasks import add as task_add
from common.data_util import get_data, build_json_error, build_json_result
# LOG = 
from common.log_utils import tcp_log, trace_log
from common.log_utils import logger as LOG
api = UserDto.admin_api
_user = UserDto.user

parser = api.parser()


@api.route('/users')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    def get(self):
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        """List all registered users"""
        LOG.error('=================---------------------- getting all user..')
        LOG.warning('=================---------------------- getting all user..')
        LOG.info(request.headers)
        return build_json_result(get_all_users(limit, offset))

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
        LOG.error('=================---------------------- get a user..')
        user = get_a_user(public_id)
        if not user:
            api.abort(404, message='Nie znaleziono użytkownika')
        else:
            return build_json_result(user)

@api.route('/change_email')
class ChangeEmailAPI(Resource):
    """
    """

    def post(self):
        post_data = request.get_json(force=True)
        isOk, message = update_email(get_data(post_data, 'account_id'), get_data(post_data, 'email'))
        if isOk:
            return build_json_result(None, 200, message)
        else:
            return build_json_result(None, 404, 'Twoja sesja wygasła', 'Your token is invalid')