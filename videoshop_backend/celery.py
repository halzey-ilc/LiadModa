# videoshop_backend/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoshop_backend.settings')

app = Celery('videoshop_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
