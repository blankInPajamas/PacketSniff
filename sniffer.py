import json
import redis
from scapy.all import IP, TCP, UDP, ICMP, sniff

# Connecting to Redis/Valkey
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0
)

class Packet:
    def __init__(self, srcIP, destIP, srcPort, dstPort, type, length, summary, payload):
        self.srcIP = srcIP
        self.destIP = destIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.type = type
        self.length = length
        self.summary = summary
        self.payload = payload


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

    packet_data = Packet(
        srcIP= srcIP,
        destIP= destIP,
        srcPort= srcPort,
        dstPort= dstPort,
        type=  protocol,
        length= length,
        summary= summary,
        payload= payload
    )

    r.publish('packet_stream', json.dumps(packet_data.__dict__))
    print(f"[{protocol}] {srcIP}:{srcPort} -> {destIP}:{dstPort}")

if __name__ == '__main__':
    INTERFACE = 'wlp0s20f3'
    print(f'Starting PacketSniff daemon on interface: {INTERFACE}...')

    sniff(iface=INTERFACE, prn=packet_parsing, store=0)