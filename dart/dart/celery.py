from __future__ import absolute_import

import logging
import os

import ecs_logging
from celery import Celery, signals
from celery.schedules import crontab
from celery.signals import setup_logging
from django.conf import settings  # noqa

# logger = logging.getLogger()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dart.settings")
app = Celery("dart")
app.config_from_object("django.conf:settings", namespace="CELERY")
#     dictConfig(settings.LOGGING)

app.conf.beat_schedule = {
    'api-call-task': {
        'task': 'corp_sync.tasks.enqueue_pending_codes',  # 작업을 실행할 함수 경로
        'schedule': 3600,  # 매일 18시에 작업 실행
        # 'schedule': crontab(minute=38, hour=19),  # 매일 18시에 작업 실행
    },
}

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@signals.after_setup_logger.connect
def setup_logger(logger, *args, **kwargs):
    logger = logging.getLogger("remote")

    if len(list(logger.handlers)) == 0:
        shandle = logging.StreamHandler()
        shandle.setFormatter(ecs_logging.StdlibFormatter(stack_trace_limit=0))

        logger.addHandler(shandle)
