release: python manage.py migrate
web: python manage.py collectstatic && gunicorn serca_project.wsgi