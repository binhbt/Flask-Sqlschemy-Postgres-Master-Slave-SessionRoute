from common.validate_util import valid_email
from common.data_util import get_data, build_json_error, build_json_result
import logging
from flask import request
from flask_restplus import Resource
from app.main.worker.mail_tasks import send_async_email
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto, UserDto
from ..util.token_util import generate_rand_token
from ..service.user_service import save_new_user, active_user, update_password, get_a_user, get_user_by_email, update_email
from ..service.active_token_service import save_token, delete_token, check_token, build_active_link
from ..service.change_pass_service import save_pass_token, delete_pass_token, check_email, build_pass_link, check_pass_token, check_pass, check_email_role
from app.main.config import mail_settings, MAIL_USERNAME, MAIL_PASSWORD, MAIL_NAME
from common.send_mail_by_sendinblue import send_email_by_sendinblue
from flask_mail import Message
from flask import current_app
from flask_mail import Mail
from common.gmail import Gmail
from common.send_mail_postfix import PostFix
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
from common.log_utils import tcp_log
api = AuthDto.api
user_auth = AuthDto.user_auth
_user = UserDto.user
from ..util.validate_util import register_validate, login_validate, send_mail_validate, change_pass_validate

@api.route('/register')
class UserRegister(Resource):
    """
        User Login Resource
    """
    @api.doc('user register')
    @api.response(201, 'User successfully registered.')
    @api.doc('register new user')
    def post(self):
        post_data = request.get_json(force=True)
        ok, err = register_validate(post_data)
        if not ok:
            return build_json_error(err, 400,'Błąd walidacji', 'Validation failed')
        if post_data['role'] != 'user' and post_data['role'] != 'provider':
            post_data['role'] = 'user'
        post_data['account_type'] = 'kidssy'
        LOG.info(post_data)
        # active_token = generate_rand_token()
        # save_token(active_token, post_data['email'])
        # send_async_email.delay(post_data['email'], 'Activate account',
        #                        build_active_link(None, active_token))
        return save_new_user(data=post_data)



@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    def post(self):
        post_data = request.get_json(force=True)
        LOG.info(post_data)
        tcp_log(post_data)
        ok, err = login_validate(post_data)
        if not ok:
            return build_json_error(err, 400, 'Błąd walidacji', 'Validation failed')
        return Auth.login_user(data=post_data)


@api.route('/login_by_facebook')
class UserLoginFacebook(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    def post(self):
        post_data = request.get_json(force=True)
        return Auth.login_facebook_user(post_data)


@api.route('/login_by_google')
class UserLoginGoogle(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    def post(self):
        post_data = request.get_json(force=True)
        return Auth.login_google_user(post_data)


@api.route('/tokens/renew')
class RenewToken(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    def post(self):
        post_data = request.get_json(force=True)
        LOG.info(post_data)
        return Auth.renew_token(get_data(post_data, 'device_id'), get_data(post_data, 'refresh_token'))


@api.route('/test')
class TestAPI(Resource):
    """
    Logout Resource
    """

    def get(self):
        # get auth token
        LOG.debug('test log %s', request.headers)
        LOG.debug('%s', request.args)
        auth_header = request.headers.get('Authorization')
        LOG.info('11111111111111111111')
        LOG.info('222222222222222222222')
        LOG.info('33333333333333333')
        LOG.info('4444444444444444444444 \n')
        LOG.info('55555555555555555555555555 \n')
        return build_json_result('Hello world')
    def post(self):
        # get auth token
        LOG.debug('%s', request.headers)
        LOG.debug('%s', request.args)
        LOG.debug('%s', request.form)
        LOG.debug('%s', request.values)
        post_data = request.get_json(force=True)
        LOG.debug('%s', post_data)
        auth_header = request.headers.get('Authorization')
        return build_json_result('Hello world')

@api.route('/task/<x1>/<x2>')
class TestTaskAPI(Resource):
    """
    Logout Resource
    """

    def get(self, x1, x2):
        from ..util.celery_util import celery
        import celery.states as states
        from flask import url_for
        # get auth token
        LOG.info(request.headers)
        LOG.info(request.args)
        auth_header = request.headers.get('Authorization')
        task = celery.send_task('tasks.add', args=[int(x1), int(x2)], kwargs={})
        response = task.id
        return response

@api.route('/task/check/<task_id>')
class TestCheckTaskAPI(Resource):
    """
    Logout Resource
    """

    def get(self, task_id):
        from ..util.celery_util import celery
        import celery.states as states
        res = celery.AsyncResult(task_id)
        if res.state == states.PENDING:
            return res.state
        else:
            return str(res.result)


@api.route('/resend_activate_mail')
class ReSendMailAPI(Resource):
    """
    Logout Resource
    """

    def post(self):
        post_data = request.get_json(force=True)
        ok, err = send_mail_validate(post_data)
        if not ok:
            return build_json_error(err, 400, 'Błąd walidacji','Validation failed')
        user = get_user_by_email(post_data['email'])
        # send_email_by_sendinblue(
        #     post_data['email'], 'Active your account', build_active_link(post_data['email'], None))
        active_token = generate_rand_token()
        save_token(active_token, post_data['email'])
        #'Activate account'
        send_email_by_sendinblue(post_data['email'], 'KIDAGO.PL - AKTYWACJA KONTA',
                                 build_active_link(None, active_token, user.role))
        return build_json_result(None, 200, 'Wysłano wiadomość email', 'email sent')



@api.route('/send_active_email/<account_id>')
class SendActiveMailAPI(Resource):
    """
    Logout Resource
    """

    def post(self, account_id):
        user = get_a_user(account_id)
        if not user:
            return build_json_result(None, 404, 'Nie znaleziono użytkownika', 'User not found')
        # send_email_by_sendinblue(
        #     user.email, 'Active your account', build_active_link(user.email, None))
        active_token = generate_rand_token()
        save_token(active_token, user.email)
        send_email_by_sendinblue(user.email, 'KIDAGO.PL - AKTYWACJA KONTA',
                                 build_active_link(None, active_token, user.role))
        return build_json_result(None, 200,'Wysłano wiadomość email', 'email sent')


@api.route('/active/<string:token>')
class ActiveUserAPI(Resource):
    """
    Logout Resource
    """

    def get(self, token):
        # get auth token
        isExist, email = check_token(token)
        if isExist:
            isOk, message = active_user(email)
            if isOk:
                return build_json_result(None, 200, message)
            else:
                return build_json_result(None, 500, message)

        else:
            return build_json_result(None, 404, 'Twoja sesja wygasła', 'Your token is invalid')


@api.route('/forgot_password')
class ForgotPasswordAPI(Resource):
    """
    Logout Resource
    """

    def post(self):
        post_data = request.get_json(force=True)
        isExist, user = check_email_role(get_data(post_data, 'email'), get_data(post_data, 'role'))
        if isExist:
            save_pass_token(token=None, email=get_data(post_data, 'email'))
            html_content = build_pass_link(get_data(post_data, 'email'), None, user.role)
            LOG.info(html_content)
            send_email_by_sendinblue(
                get_data(post_data, 'email'), 'Zresetuj hasło', html_content)
            return build_json_result(None, 200, 'Wysłano wiadomość email', 'email sent')
        else:
            return build_json_result(None, 404, 'Nie znaleziono adresu email', 'email not exist')


@api.route('/change_password/<string:token>')
class ChangePasswordAPI(Resource):
    """
    Logout Resource
    """

    def post(self, token):
        post_data = request.get_json(force=True)
        ok, err = change_pass_validate(post_data)
        if not ok:
            return build_json_error(err, 400, 'Błąd walidacji','Validation failed')
        isExist, email = check_pass_token(token)
        if isExist:
            isOk, message = update_password(
                email, get_data(post_data, 'password'))
            if isOk:
                return build_json_result(None, 200, message)
            else:

                return build_json_result(None, 500, message)
        else:
            return build_json_result(None, 404, 'Twoja sesja wygasła', 'Your token is invalid')



@api.route('/change_password')
class ChangePasswordAPI2(Resource):
    """
    Logout Resource
    """

    def post(self):
        post_data = request.get_json(force=True)
        ok, err = change_pass_validate(post_data)
        if not ok:
            return build_json_error(err, 400, 'Błąd walidacji', 'Validation failed')
        isExist, email = check_pass(
            get_data(post_data, 'account_id'), get_data(post_data, 'old_password'))
        if isExist:
            isOk, message = update_password(
                email, get_data(post_data, 'password'))
            if isOk:

                return build_json_result(None, 200, message)
            else:

                return build_json_result(None, 500, message)

        else:
            return build_json_result(None, 404, 'Stare haslo jest niepoprawne', 'Your old password is not correct')
