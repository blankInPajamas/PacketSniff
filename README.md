# PacketSniff 

**PacketSniff** is a lightweight, web-based network traffic analyzer and `.pcap` explorer built with Django. Designed as a browser-accessible alternative to desktop tools like Wireshark, it enables real-time packet capture, deep protocol inspection, dynamic bandwidth visualization, and offline PCAP file analysis.


## Key Features

* **Live Packet Capture:** Stream live network interface traffic directly to the browser using Django Channels and Redis.
* **Wireshark-Style Inspection:** Interactive packet table with protocol color coding, hierarchical header inspection, and raw Hex/ASCII payload views.
* **PCAP File Explorer:** Upload `.pcap` and `.pcapng` files for offline analysis and bulk parsing powered by Celery background workers.
* **Real-Time Analytics:** Dynamic dashboards visualizing bandwidth consumption, protocol distributions, and top talkers.
* **Privilege Isolation:** Designed to run packet captures via isolated worker daemons, keeping your primary Django application secure.


## Initialize Project

To initialize the project, create a virtual python environment.

```bash
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install django

# Verify installation
python -m django --version
```