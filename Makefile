.PHONY: run migrate migrations sniff

run:
	./venv/bin/python manage.py runserver

migrations:
	./venv/bin/python manage.py makemigrations

migrate:
	./venv/bin/python manage.py migrate

sniff:
	sudo ./venv/bin/python sniffer.py
	