import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
app = Celery('rest')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
