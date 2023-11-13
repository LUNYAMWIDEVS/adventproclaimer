release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:$PORT
celery: celery -A eLMS worker --beat --scheduler django --loglevel=info