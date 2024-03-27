#!/bin/bash

python manage.py collectstatic --no-input
# i commit my migration files to git so i dont need to run it on server
# ./manage.py makemigrations app_name
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# here it start nginx and the uwsgi
#supervisord -c /etc/supervisor/supervisord.conf -n

# Run Server
python manage.py runserver 0.0.0.0:8000
