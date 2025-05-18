web: gunicorn videoshop_backend.wsgi:application --bind 0.0.0.0:8000
worker: celery -A videoshop_backend worker -Q high,default -n worker@%h --loglevel=info
worker: celery -A videoshop_backend worker --loglevel=info

