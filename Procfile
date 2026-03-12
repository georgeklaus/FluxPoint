release: python manage.py migrate
web: gunicorn backend.fluxpoint.wsgi --bind 0.0.0.0:$PORT --workers 1
