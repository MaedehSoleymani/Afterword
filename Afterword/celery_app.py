import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Afterword.settings.development')

app=Celery('Afterword')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_due_messages': {
        'task': 'outbox.tasks.send_due_messages',
        'schedule': 10.0,
    },
    'check_inactive_users': {
        'task': 'outbox.tasks.check_inactive_users',
        'schedule': 3600.0,
    },
}

app.conf.timezone = 'UTC'