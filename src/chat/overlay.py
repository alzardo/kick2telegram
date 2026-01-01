# -*- coding: utf-8 -*-
"""
FFmpeg streaming with chat overlay support.

Uses Streamlink to capture a Kick stream and FFmpeg to add a text overlay
with live chat messages before sending to Telegram RTMP.
"""
import subprocess
import re

import cloudscraper

from .. import config


def get_kick_hls_stream(channel):
    """
    Gets the HLS stream URL for a Kick channel.

    Args:
        channel (str): The Kick channel name.

    Returns:
        tuple: (m3u8_url, scraper) if found, (None, None) otherwise.
    """
    scraper = cloudscraper.create_scraper()
    url = f"https://kick.com/{channel}"
    try:
        page = scraper.get(url, timeout=10).text
        m3u8_urls = re.findall(r'https://[^\s"\']+?\.m3u8', page)
        if m3u8_urls:
            print(f"HLS URL found: {m3u8_urls[0]}")
            return m3u8_urls[0], scraper
        else:
            print("No .m3u8 URL found on the page.")
            return None, None
    except Exception as e:
        print(f"Error getting HLS stream: {e}")
        return None, None


def start_stream_with_overlay(channel, chat_file="chat.txt", font_path="/Windows/Fonts/arial.ttf"):
    """
    Starts streaming with chat overlay using Streamlink and FFmpeg.

    This function pipes Streamlink output through FFmpeg, adding a text overlay
    with chat messages from the specified file.

    Args:
        channel (str): The Kick channel name.
        chat_file (str): Path to the file containing chat messages.
        font_path (str): Path to the font file for the overlay.
    """
    kick_url = f"https://kick.com/{channel}"
    rtmp_url = config.RTMP_DEST

    print(f"🎬 Starting stream from: {kick_url}")
    print(f"📡 Streaming to Telegram: {rtmp_url}")

    try:
        # Streamlink command
        streamlink_cmd = [
            "streamlink",
            kick_url,
            "best",
            "-O"  # Output to stdout
        ]

        # FFmpeg command with chat overlay
        ffmpeg_cmd = [
            "ffmpeg",
            "-re",
            "-i", "pipe:0",  # Input from streamlink
            "-vf",
            (
                f"drawtext=textfile={chat_file}:"
                "reload=1:"
                "fontcolor=white:"
                "fontsize=22:"
                "x=20:"
                "y=20:"
                "line_spacing=1:"
                f"fontfile={font_path}:"
                "box=1:"
                "boxcolor=black@0.5:"
                "boxborderw=10"
            ),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-c:a", "aac",
            "-f", "flv",
            rtmp_url
        ]

        # Launch streamlink and pipe output to ffmpeg
        streamlink_proc = subprocess.Popen(streamlink_cmd, stdout=subprocess.PIPE)
        ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=streamlink_proc.stdout)

        # Wait for completion
        ffmpeg_proc.wait()
        print("🛑 Stream finished.")

    except Exception as e:
        print(f"❌ Error during streaming: {e}")
