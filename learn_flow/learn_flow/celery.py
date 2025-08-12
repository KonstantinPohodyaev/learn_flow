import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_flow.settings')

app = Celery('learn_flow')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()