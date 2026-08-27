.PHONY: run migrate migrations

run:
	./venv/bin/python manage.py runserver

migrations:
	./venv/bin/python manage.py makemigrations

migrate:
	./venv/bin/python manage.py migrate
	