import os
from celery import Celery
from kombu import Queue

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoshop_backend.settings')

# Создаём приложение Celery
app = Celery('videoshop_backend')

# Загружаем настройки из Django (используем prefix 'CELERY_')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим все задачи в приложениях
app.autodiscover_tasks()

# Очереди с приоритетами
app.conf.task_queues = (
    Queue('default'),
    Queue('high'),
    Queue('low'),
)

# Очередь по умолчанию
app.conf.task_default_queue = 'default'

# (опционально) настройки повтора задач
app.conf.task_annotations = {
    '*': {'rate_limit': '20/s'}  # или retry, если нужно
}
