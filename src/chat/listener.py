# -*- coding: utf-8 -*-
"""
WebSocket listener for Kick.com chat messages.

Connects to Kick's Pusher WebSocket to receive real-time chat messages.
"""
import asyncio
import json
import textwrap
from collections import deque

import websockets
import cloudscraper


def get_chatroom_id(username):
    """
    Gets the chatroom ID for a Kick channel.

    Args:
        username (str): The Kick channel username.

    Returns:
        int or None: The chatroom ID if found, otherwise None.
    """
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/api/v1/channels/{username}"

    try:
        response = scraper.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            chatroom = data.get("chatroom")
            if chatroom:
                return chatroom.get("id")
            else:
                print("Channel does not have an available chatroom.")
        else:
            print(f"Error {response.status_code}: Could not access channel '{username}'.")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None


def split_message(text, width=40):
    """
    Splits a message into multiple lines with a maximum width.

    Args:
        text (str): The text to split.
        width (int): Maximum characters per line.

    Returns:
        list: List of text lines.
    """
    return textwrap.wrap(text, width=width)


async def listen_chat(chatroom_id, output_file="chat.txt", max_messages=20, line_width=60):
    """
    Listens to chat messages from a Kick chatroom via WebSocket.

    Args:
        chatroom_id (int): The chatroom ID to listen to.
        output_file (str): File path to write chat messages.
        max_messages (int): Maximum number of messages to keep in history.
        line_width (int): Maximum characters per line for wrapping.
    """
    ws_url = "wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=7.6.0"
    messages = deque(maxlen=max_messages)

    async with websockets.connect(ws_url) as websocket:
        join_payload = {
            "event": "pusher:subscribe",
            "data": {
                "auth": "",
                "channel": f"chatrooms.{chatroom_id}.v2"
            }
        }
        await websocket.send(json.dumps(join_payload))
        print(f"🟢 Listening to chatroom ID {chatroom_id}...\n")

        while True:
            try:
                msg = await websocket.recv()
                payload = json.loads(msg)

                if payload.get("event") == "App\\Events\\ChatMessageEvent":
                    message_data = json.loads(payload["data"])
                    username = message_data["sender"]["username"]
                    content = message_data["content"]
                    formatted_message = f"{username}: {content}"

                    # Split into lines with maximum width
                    lines = split_message(formatted_message, width=line_width)

                    # Add each line to history
                    for line in lines:
                        messages.append(line)

                    # Write all messages to output file
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write("\n".join(messages))

            except Exception as e:
                print(f"⚠️ WebSocket error: {e}")
                break


def start_chat_listener(channel_name, output_file="chat.txt"):
    """
    Starts the chat listener for a channel.

    Args:
        channel_name (str): The Kick channel name.
        output_file (str): File path to write chat messages.
    """
    chatroom_id = get_chatroom_id(channel_name)
    if chatroom_id:
        asyncio.run(listen_chat(chatroom_id, output_file))
    else:
        print(f"❌ Could not get chatroom ID for channel '{channel_name}'.")
