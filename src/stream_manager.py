# -*- coding: utf-8 -*-
"""
Module for managing the FFmpeg streaming process.
"""
import subprocess
from . import config


def start_stream(m3u8_url):
    """
    Starts the FFmpeg process to restream the source.

    Args:
        m3u8_url (str): The source stream URL.

    Returns:
        subprocess.Popen: The started FFmpeg process object.
    """
    ffmpeg_command = [
        "ffmpeg",
        "-i", m3u8_url,
        "-c:v", "copy",
        "-c:a", "aac",
        "-ar", "44100",
        "-b:a", "128k",
        "-f", "flv",
        config.RTMP_DEST
    ]
    
    print(f"Executing FFmpeg command: {' '.join(ffmpeg_command)}")
    
    # Start ffmpeg without displaying its output in our console
    ffmpeg_process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print("FFmpeg process started.")
    return ffmpeg_process
