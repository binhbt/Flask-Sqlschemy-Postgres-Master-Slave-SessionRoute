from celery import Celery
from app.main.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import logging
LOG = logging.getLogger('celery')
# LOG.debug('###################### -------------- send_async_email'+CELERY_BROKER_URL)
celery = Celery('project_worker',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND,
                include=['app.main.worker.tasks', 'app.main.worker.mail_tasks'])
celery.config_from_object('app.main.worker.celeryconfig')
