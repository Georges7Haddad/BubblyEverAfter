cd /app
python manage.py collectstatic --no-input
python manage.py migrate

gunicorn --bind :8000 --workers 3 BubblyEverAfter.wsgi:application