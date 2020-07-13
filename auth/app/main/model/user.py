
import datetime

from .. import db, flask_bcrypt
# NOTE: commented import below will lead to bellow error, need to investigate about this error
# sqlalchemy.exc.InvalidRequestError: Table 'user' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
# from app.main import db, flask_bcrypt

from app.main.model.active_token import BlacklistToken
from app.main.config import key, AuthConfig, REDIS_URL
import jwt
import logging
# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(50))
    avatar = db.Column(db.String(250))
    role = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    active_on = db.Column(db.DateTime, nullable=True)
    last_logged = db.Column(db.DateTime, nullable=True)
    account_type = db.Column(db.String(50))
    facebook_id = db.Column(db.String(50))
    google_id = db.Column(db.String(50))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id, role, account_type='kidssy'):
        iss = AuthConfig.USER_KEY
        secret = AuthConfig.USER_SECRET
        if role == 'admin':
            iss = AuthConfig.ADMIN_KEY
            secret = AuthConfig.ADMIN_SECRET
        if role == 'provider':
            iss = AuthConfig.PROVIDER_KEY
            secret = AuthConfig.PROVIDER_SECRET
        # LOG.info(iss)
        # LOG.info(secret)
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=AuthConfig.EXP_TIME, seconds=600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'iss': iss,
                'role': role,
                'atype':account_type
            }
            return jwt.encode(
                payload,
                secret,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
