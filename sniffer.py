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
    if IP not in packet:
        return

    srcIP = packet[IP].src
    destIP = packet[IP].dst
    length = len(packet)
    summary = packet.summary()

    protocol = 'OTHER'
    srcPort = None
    dstPort = None

    if TCP in packet:
        protocol = "TCP"
        srcPort = packet[TCP].sport
        dstPort = packet[TCP].dport
    elif UDP in packet:
        protocol = 'UDP'
        srcPort = packet[UDP].sport
        dstPort = packet[UDP].dport
    elif ICMP in packet:
        protocol = 'ICMP'

    payload = ''
    if packet.haslayer('Raw'):
        payload = packet['Raw'].load.hex()

    # Use a raw dict directly (avoiding custom class collision with Scapy.Packet)
    packet_data = {
        "srcIP": srcIP,
        "destIP": destIP,
        "srcPort": srcPort,
        "dstPort": dstPort,
        "type": protocol,
        "length": length,
        "summary": summary,
        "payload": payload
    }

    # Broadcast directly to Django Channels
    async_to_sync(channel_layer.group_send)(
        "packets",
        {
            "type": "packet.message",
            "data": packet_data,
        }
    )

    print(f"[{protocol}] {srcIP}:{srcPort} -> {destIP}:{dstPort}")
    
    # Return None explicitly so Scapy does not attempt serialization
    return None

if __name__ == '__main__':
    INTERFACE = 'wlp0s20f3'
    print(f'Starting PacketSniff daemon on interface: {INTERFACE}...')
    sniff(iface=INTERFACE, prn=packet_parsing, store=0)