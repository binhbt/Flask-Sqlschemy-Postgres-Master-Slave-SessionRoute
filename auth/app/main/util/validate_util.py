from common.validate_util import validate_data


def register_validate(data):
    schema = {'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': True},
              'password': {'type': 'string', 'minlength': 6, 'required': True, 'regex': '^(?=.*[A-Za-z@$!%*#?&])(?=.*\d)[A-Za-z@$!%*#?&\d]{6,}$'},
              'role': {'type': 'string', 'required': True}}
    return validate_data(data, schema)


def login_validate(data):
    schema = {'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': True},
              'password': {'type': 'string', 'minlength': 6, 'required': True, 'regex': '^(?=.*[A-Za-z@$!%*#?&])(?=.*\d)[A-Za-z@$!%*#?&\d]{6,}$'}}
    return validate_data(data, schema)


def send_mail_validate(data):
    schema = {'email': {'type': 'string',
                        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': True}}
    return validate_data(data, schema)


def change_pass_validate(data):
    schema = {'password': {'type': 'string',
                           'minlength': 6, 'required': True, 'regex': '^(?=.*[A-Za-z@$!%*#?&])(?=.*\d)[A-Za-z@$!%*#?&\d]{6,}$'}}
    return validate_data(data, schema)
