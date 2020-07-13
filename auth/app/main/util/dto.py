from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    admin_api = Namespace('admin', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(description='account id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'account_type': fields.String(required=True, description='user username'),
        'facebook_id': fields.String(required=True, description='facebook_id'),
        'last_logged': fields.String(required=True, description='last_logged'),
        'google_id': fields.String(required=True, description='google_id'),
        'role': fields.String(required=True, description='user password')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.Integer(description='account id'),
        'email': fields.String(required=True, description='The email address'),
        'role': fields.String(required=True, description='The user password '),
    })
