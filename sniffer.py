import os
import django
from scapy.all import IP, TCP, UDP, ICMP, sniff
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Setup Django environment so Scapy script can access Channels Layer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'packetsniff.settings')
django.setup()

channel_layer = get_channel_layer()

def packet_parsing(packet):
    # 1. Parse IP Layer using string names to avoid import conflicts
    if packet.haslayer('IP'):
        network_layer = packet.getlayer('IP')
    elif packet.haslayer('IPv6'):
        network_layer = packet.getlayer('IPv6')
    else:
        # Ignore non-IP frames (ARP, L2 noise) completely
        return None

    # Explicitly cast to string to prevent JSON serialization drops
    src_ip = str(network_layer.src)
    dest_ip = str(network_layer.dst)

    # 2. Parse Transport Layer
    protocol = "OTHER"
    src_port = None
    dst_port = None

    if packet.haslayer('TCP'):
        protocol = "TCP"
        transport = packet.getlayer('TCP')
        src_port = int(transport.sport)
        dst_port = int(transport.dport)
    elif packet.haslayer('UDP'):
        protocol = "UDP"
        transport = packet.getlayer('UDP')
        src_port = int(transport.sport)
        dst_port = int(transport.dport)
    elif packet.haslayer('ICMP'):
        protocol = "ICMP"

    # 3. Extract Payload
    payload_hex = ""
    if packet.haslayer('Raw'):
        payload_hex = packet.getlayer('Raw').load.hex()
    elif packet.payload:
        payload_hex = bytes(packet.payload).hex()

    # 4. Strictly Formatted Dictionary
    packet_data = {
        "type": protocol,
        "srcIP": src_ip,
        "destIP": dest_ip,
        "srcPort": src_port,
        "dstPort": dst_port,
        "length": int(len(packet)),
        "summary": str(packet.summary()),
        "payload": payload_hex
    }

    # 5. Broadcast to Django Channels
    async_to_sync(channel_layer.group_send)(
        "packets",
        {
            "type": "packet.message",
            "data": packet_data,
        }
    )

    print(f"[{protocol}] {src_ip}:{src_port} -> {dest_ip}:{dst_port}")
    return None

if __name__ == '__main__':
    INTERFACE = 'wlp0s20f3'
    print(f'Starting PacketSniff daemon on interface: {INTERFACE}...')
    sniff(iface=INTERFACE, prn=packet_parsing, store=0)