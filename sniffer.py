import redis
from scapy.all import IP

# Connecting to Redis/Valkey
r = redis.Redis(
    host="localhost",
    port=6000,
    db=0
)

# capture_session = models.ForeignKey(CaptureSession, on_delete=models.CASCADE, related_name='packets')
#     timestamp = models.DateTimeField()

#     sourceIP = models.GenericIPAddressField()
#     destIP = models.GenericIPAddressField()

#     sourcePort = models.IntegerField(null=True, blank=True)
#     destPort = models.IntegerField(null=True, blank=True)

#     protocol_type = models.CharField(max_length=20) # TCP, UDP, ICMP, DNS
#     packet_length = models.IntegerField()

#     summary = models.TextField()

#     payload = models.TextField(blank=True, null=True)

class Packet:
    def __init__(self, srcIP, destIP, srcPort, destPort, type, length, summary, payload):
        self.srcIP = srcIP
        self.destIP = destIP
        self.srcPort = srcPort
        self.destPort = destPort
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

    pass