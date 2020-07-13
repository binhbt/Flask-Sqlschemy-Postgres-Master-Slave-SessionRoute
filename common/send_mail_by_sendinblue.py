import logging
from app.main.config import mail_settings, MAIL_USERNAME, MAIL_PASSWORD, MAIL_NAME

# LOG = logging.getLogger('app')
from common.log_utils import logger as LOG
def send_email_by_sendinblue(touser, title, body):
    import requests
    API_ENDPOINT = "https://api.sendinblue.com/v3/smtp/email"
    API_KEY = "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"
    data = {'name': 'Campaign sent via the API',
            'subject': title,
            'sender': {"name": MAIL_NAME, "email": MAIL_USERNAME},
            'type': 'classic',
            "htmlContent": body,
            "to": [
                {
                    "email": touser
                    # "name": "John Doe"
                }
            ]}
    headers = {"accept": "application/json",
                "api-key": API_KEY,
                "content-type": "application/json"}
    r = requests.post(url=API_ENDPOINT, json=data, headers=headers)
    pastebin_url = r.text
    LOG.info(pastebin_url)

def send_active_account(account_id):
    import requests
    LOG.debug('###################### -------------- send_async_email')
    """ Background task to send an email with Flask-Mail."""
    url='http://auth:5000/api/v1/auth/send_active_email/'+str(account_id)
    response = requests.post(url)
    print(response)
    LOG.debug(response)
