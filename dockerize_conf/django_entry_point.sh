python3.7 /manage.py migrate
celery -A URLShortener worker -l info --detach
uwsgi --ini /dockerize_conf/uwsgi.ini
