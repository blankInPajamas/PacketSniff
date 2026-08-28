.PHONY: run migrate migrations sniff dev

run:
	./venv/bin/daphne -b 127.0.0.1 -p 8000 packetsniff.asgi:application

migrations:
	./venv/bin/python manage.py makemigrations

migrate:
	./venv/bin/python manage.py migrate

sniff:
	sudo ./venv/bin/python sniffer.py
	
dev:
	@echo "Starting PacketSniff (Daphne + Sniffer)..."
	@trap 'kill %1' EXIT; \
	./venv/bin/daphne -b 127.0.0.1 -p 8000 packetsniff.asgi:application & \
	sudo ./venv/bin/python sniffer.py