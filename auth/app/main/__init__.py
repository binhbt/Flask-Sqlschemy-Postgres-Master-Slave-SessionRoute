import os
from flask import Flask
from logging.config import dictConfig as logging_dict_config

from app.main.config import config_by_name, ENABLE_CORS, LOGGING

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.main.config import mail_settings
from common.flask_routing_session import RouteSQLAlchemy
# db = SQLAlchemy()




flask_bcrypt = Bcrypt()


def get_working_env():
    env = os.environ.get('WORKING_ENV', 'dev')
    if env not in ['dev', 'test', 'stag', 'prod']:
        raise ValueError('Set working environment: export WORKING_ENV=[dev/test/stag/prod]')
    return env


# def create_app():
#     env = get_working_env()

#     app = Flask(__name__)

#     logging_config(app)

#     app.config.from_object(config_by_name[env])
#     app.config.update(mail_settings)

#     configure_extensions(app)
#     register_blueprints(app)


#     return app


def configure_extensions(app):
    from app.main.model import user, active_token
    """configure flask extensions
    """
    db.init_app(app)
    flask_bcrypt.init_app(app)

    if ENABLE_CORS:
        from flask_cors import CORS
        CORS(app)


def register_blueprints(app):
    """register all blueprints for application
    """
    from flask_restplus import Api
    from flask import Blueprint

    from app.main.controller.user_controller import api as user_ns
    from app.main.controller.auth_controller import api as auth_ns
    from app.main.controller.admin_controller import api as admin_ns
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

    api = Api(blueprint,
              title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
              version='1.0',
              description='a boilerplate for flask restplus web service'
              )

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(admin_ns)
    app.register_blueprint(blueprint)


def logging_config(app):
    # print(app.logger.name)
    app.logger
    logging_dict_config(LOGGING)

# app = create_app()


env = get_working_env()

app = Flask(__name__)

logging_config(app)

app.config.from_object(config_by_name[env])
app.config.update(mail_settings)

db = RouteSQLAlchemy(app)

configure_extensions(app)
register_blueprints(app)
