import os
from celery import Celery

# Установите переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kursach.settings')

app = Celery('kursach')

# Загрузите настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаружьте задачи в приложениях Django
app.autodiscover_tasks()