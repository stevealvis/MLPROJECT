web: gunicorn disease_prediction.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput

