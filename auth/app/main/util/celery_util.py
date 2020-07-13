import os
from celery import Celery
from app.main.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery = Celery('kidssy_worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
