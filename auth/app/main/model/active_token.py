from .. import db
import datetime


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
class ActiveToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'active_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email =db.Column(db.String(500), nullable=False )
    token = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_token(auth_token):
        # check whether auth token has been blacklisted
        res = ActiveToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
class ChangePassToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'change_pass_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email =db.Column(db.String(500), nullable=False )
    token = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.created_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_token(auth_token):
        # check whether auth token has been blacklisted
        res = ActiveToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
class Device(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id =db.Column(db.String(500), nullable=False)
    device_name = db.Column(db.String(500), nullable=True)
    device_model = db.Column(db.String(500), nullable=True)
    refresh_token = db.Column(db.String(500), nullable=False)
    expired_time = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, device_id, device_name, device_model, refresh_token, expired_time):
        self.user_id = user_id
        self.device_id = device_id
        self.device_name = device_name
        self.device_model = device_model
        self.refresh_token = refresh_token
        self.expired_time = expired_time
        self.created_on = datetime.datetime.now()

    # def __repr__(self):
    #     return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_token(auth_token):
        # check whether auth token has been blacklisted
        res = ActiveToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False