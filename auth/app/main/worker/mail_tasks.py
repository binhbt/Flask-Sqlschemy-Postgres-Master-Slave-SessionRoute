from app.main.worker.celery_app import celery
import logging

# from flask_mail import Message
# from flask import current_app
# from flask_mail import Mail
LOG = logging.getLogger('celery')
import requests

@celery.task(name='send_async_email')
def send_async_email(touser, title, body):
    LOG.debug('###################### -------------- send_async_email')
    """ Background task to send an email with Flask-Mail."""
    payload = {'touser': touser, 'title':title, 'body':body}
    url='http://auth:5000/api/v1/auth/send_activate_mail'
    print(payload)
    response = requests.post(url, json = payload)
    print(response)
    LOG.debug(response)
