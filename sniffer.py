import os
import sys
import asyncio
import django
from scapy.all import IP, TCP, UDP, ICMP, sniff
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'packetsniff.settings')
django.setup()

channel_layer = get_channel_layer()

INTERFACE = 'wlp0s20f3'
current_bpf_filter = sys.argv[1] if len(sys.argv) > 1 else ""
should_restart = False

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

def stop_filter_check(packet):
    """Signals Scapy to break the sniff loop when a new filter is received."""
    global should_restart
    return should_restart

def run_sniff_loop():
    """Runs Scapy sniff synchronously until interrupted or signaled to restart."""
    global current_bpf_filter, should_restart
    should_restart = False

    print(f"[*] Sniffing on {INTERFACE} | BPF: '{current_bpf_filter}'")
    try:
        sniff(
            iface=INTERFACE,
            prn=packet_parsing,
            filter=current_bpf_filter,
            stop_filter=stop_filter_check,
            store=0
        )
    except Exception as e:
        print(f"[!] BPF Filter Error ('{current_bpf_filter}'): {e}")
        current_bpf_filter = ""

async def control_listener():
    """Listens on the Redis 'sniffer_control' group for live filter commands."""
    global current_bpf_filter, should_restart
    
    channel = await channel_layer.new_channel()
    await channel_layer.group_add("sniffer_control", channel)

    while True:
        message = await channel_layer.receive(channel)
        if message.get("type") == "update_bpf":
            current_bpf_filter = message.get("filter", "")
            print(f"\n[!] BPF filter changed from UI: '{current_bpf_filter}'")
            should_restart = True

async def main():
    asyncio.create_task(control_listener())
    loop = asyncio.get_event_loop()

    while True:
        await loop.run_in_executor(None, run_sniff_loop)
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Sniffer daemon stopped.")