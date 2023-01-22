from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

from bank.settings import RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, RABBITMQ_VHOST

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')

app = Celery(
    'bank',
    broker='amqp://' + RABBITMQ_USER + ':' + RABBITMQ_PASSWORD + '@' + RABBITMQ_HOST + '/' + RABBITMQ_VHOST,
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = "America/Mexico_City"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task
def test(arg):
    return arg


app.conf.beat_schedule = {}
