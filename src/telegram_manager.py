# -*- coding: utf-8 -*-
"""
Module for managing Telegram interactions.
"""
import random
from telethon import TelegramClient
from telethon.tl.functions.phone import CreateGroupCallRequest, DiscardGroupCallRequest
from . import config


class TelegramManager:
    def __init__(self):
        """Initializes the Telegram client."""
        self.client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
        self.call = None
        self.group = None

    async def start(self):
        """Connects the client to Telegram."""
        print("Connecting to Telegram...")
        await self.client.start(config.PHONE)
        self.group = await self.client.get_entity(config.GROUP_ID)
        print("Connected to Telegram and group retrieved.")

    async def start_group_call(self):
        """Starts a new group call with RTMP enabled."""
        if not self.client.is_connected():
            raise ConnectionError("Telegram client is not connected.")
        try:
            print("Starting Telegram group call...")
            self.call = await self.client(CreateGroupCallRequest(
                peer=self.group,
                rtmp_stream=True,
                random_id=random.getrandbits(31)
            ))
            print("Group call started.")
            return True
        except Exception as e:
            print(f"Error starting group call: {e}")
            return False

    async def end_group_call(self):
        """Ends the active group call."""
        if self.call:
            try:
                print("Ending Telegram group call...")
                # Extract InputGroupCall object from Updates object
                if hasattr(self.call, 'updates') and len(self.call.updates) > 0 and hasattr(self.call.updates[0], 'call'):
                    input_group_call = self.call.updates[0].call
                    await self.client(DiscardGroupCallRequest(call=input_group_call))
                    print("Group call ended.")
                else:
                    print("Could not find a valid group call object to end.")
            except Exception as e:
                print(f"Error ending group call: {e}")
            finally:
                self.call = None
                
    async def disconnect(self):
        """Disconnects the Telegram client."""
        if self.client.is_connected():
            print("Disconnecting from Telegram...")
            await self.client.disconnect()
            print("Disconnected from Telegram.")
