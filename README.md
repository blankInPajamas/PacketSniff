# PacketSniff

PacketSniff is a web-based network traffic analyzer and PCAP explorer built on Django. Designed as a browser-accessible alternative to desktop utilities like Wireshark, it enables real-time packet capture, deep protocol inspection, dynamic bandwidth visualization, and offline PCAP file analysis.

## Key Features

* **Live Packet Capture:** Stream live network interface traffic directly to the browser using Django Channels and Redis.
* **Protocol Inspection:** Interactive packet table with protocol classification, header inspection, and raw payload views.
* **PCAP File Explorer:** Upload `.pcap` and `.pcapng` files for offline analysis and background parsing via Celery.
* **Real-Time Analytics:** Dashboards visualizing bandwidth consumption, protocol distributions, and top talkers.
* **Privilege Isolation:** Designed to run packet captures via isolated worker daemons, maintaining security by ensuring the primary Django process does not require root permissions.


## Project Structure

```text
PacketSniff/
├── Makefile                # Shortcuts for server, migrations, and sniffer execution
├── README.md               # Project documentation
├── manage.py               # Django management script
├── analyzer/               # Primary Django application
│   ├── admin.py            # Model registration for Django Admin
│   ├── apps.py             # App configuration metadata
│   ├── migrations/         # Database migration files (0001_initial.py)
│   ├── models.py           # CaptureSession and PacketRecord schemas
│   ├── tests.py            # Application unit tests
│   ├── urls.py             # App-level routing rules
│   └── views.py            # Request handlers and business logic
└── packetsniff/            # Project configuration package
    ├── asgi.py             # ASGI entry point for WebSockets/Django Channels
    ├── settings.py         # Global Django configuration settings
    ├── urls.py             # Root URL routing
    └── wsgi.py             # WSGI entry point for standard HTTP deployment

```


## Project Setup & Usage

### 1. Prerequisites

Ensure Python 3, Redis, and `libpcap` dependencies are installed on your system.

### 2. Virtual Environment & Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade package manager
pip install --upgrade pip

# Install project dependencies
pip install django redis scapy

```

### 3. Database Management

Apply the database migrations to set up the SQLite schema for `CaptureSession` and `PacketRecord`:

```bash
make migrate

```

### 4. Running the Development Server

```bash
make run

```


## Roadmap & Implementation Status

* [x] **Phase 1: Foundation & Data Architecture**
    * Django project and `analyzer` app setup.
    * Defined database schemas (`CaptureSession`, `PacketRecord`).
    * Generated and executed initial database migrations.
    * Configured project Makefile for task automation.


* [x] **Phase 2: Isolated Packet Ingestion Engine**
    * Develop a standalone `scapy` sniffer daemon with root privileges.
    * Implement Redis publishing pipeline for real-time packet serialization.


* [ ] **Phase 3: Asynchronous WebSockets Pipeline**
    * Configure Django Channels and Redis Channel Layer.
    * Implement WebSocket consumers to stream packet data to connected clients.


* [ ] **Phase 4: Web UI & Visualizations**
    * Build live packet inspection table with protocol color-coding.
    * Implement raw Hex/ASCII payload viewer and Chart.js dashboards.


* [ ] **Phase 5: Offline PCAP Upload Engine**
    * Implement asynchronous PCAP parsing tasks using Celery and PyShark.