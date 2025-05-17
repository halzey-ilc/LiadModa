web: gunicorn videoshop_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A videoshop_backend worker -Q high,default -n worker@%h --loglevel=info
