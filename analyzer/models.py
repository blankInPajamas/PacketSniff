from django.db import models

# Create your models here.
class CaptureSession(models.Model):
    session_name = models.CharField(max_length=255)
    interface = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_packet = models.IntegerField(default=0)
    pcap_file = models.FileField(upload_to="pcaps/", blank=True, null=True)

    def __str__(self):
        return f"{self.session_name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class PacketRecord(models.Model):
    capture_session = models.ForeignKey(CaptureSession, on_delete=models.CASCADE, related_name='packets')
    timestamp = models.DateTimeField()

    sourceIP = models.GenericIPAddressField()
    destIP = models.GenericIPAddressField()

    sourcePort = models.IntegerField(null=True, blank=True)
    destPort = models.IntegerField(null=True, blank=True)

    protocol_type = models.CharField(max_length=20) # TCP, UDP, ICMP, DNS
    packet_length = models.IntegerField()

    summary = models.TextField()

    payload = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[{self.protocol_type}] {self.source_ip}:{self.source_port} -> {self.dest_ip}:{self.dest_port}"