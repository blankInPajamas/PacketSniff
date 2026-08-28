import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CapturedPacket
from channels.db import database_sync_to_async

class PacketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'packets'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print("[Consumer CONNECTED] Client connected to WebSocket group")

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        print("[Consumer DISCONNECTED]")

    async def packet_message(self, event):
        # print(f"[PACKET RECEIVED IN CONSUMER] Raw event: {event}")
        data = event.get("data", event.get("packet"))

        await self.send(text_data=json.dumps(
            {
                "packet": data
            }
        ))

        await self.save_packet_to_db(data)

    @database_sync_to_async
    def save_packet_to_db(self, data):
        try:
            obj = CapturedPacket.objects.create(
                src_ip = data.get('src_ip', '0.0.0.0'),
                dest_ip=data.get('dest_ip', '0.0.0.0'),
                src_port=data.get('srcPort'),
                dest_port=data.get('dstPort'),
                protocol_type=data.get('type', 'OTHER'),
                length=data.get('length', 0),
                payload=data.get('payload', '')
            )
            print(f"[SUCCESS] Saved packet to DB with ID: {obj.id}")
        except Exception as e:
            print(f'DB error: Failed to persist packet {e}')