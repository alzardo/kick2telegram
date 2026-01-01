# -*- coding: utf-8 -*-
"""
Module for interacting with the Kick.com API.
"""
import time
from curl_cffi import requests


def get_kick_stream_status(channel_name):
    """
    Queries the Kick.com API to check if a channel is live.

    Args:
        channel_name (str): The Kick channel name to check.

    Returns:
        tuple: A tuple containing:
            - str: "live", "offline", or "error".
            - str or None: The m3u8 URL if live, otherwise None.
    """
    api_url = f"https://kick.com/api/v1/channels/{channel_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Querying API: {api_url}")
        response = requests.get(api_url, headers=headers, impersonate="chrome", timeout=20)
        response.raise_for_status()
        data = response.json()

        if data.get("livestream") and data["livestream"].get("is_live"):
            m3u8_url = data.get("playback_url")
            if m3u8_url:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] API indicates stream is LIVE. URL: {m3u8_url}")
                return "live", m3u8_url
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] API indicates stream is live, but playback_url not found.")
                return "offline", None
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] API indicates stream is offline.")
            return "offline", None

    except requests.exceptions.HTTPError as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] HTTP error connecting to Kick API: {e.response.status_code}")
        return "error", None
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unexpected error querying Kick API: {e}")
        return "error", None
