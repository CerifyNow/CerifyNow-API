run:
	python manage.py runserver 0.0.0.0:8000

mig:
	python manage.py makemigrations institutions
	python manage.py makemigrations users
	python manage.py migrate

admin:
	python manage.py createsuperuser

static:
	python manage.py collectstatic