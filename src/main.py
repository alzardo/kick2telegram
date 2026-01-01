# -*- coding: utf-8 -*-
"""
Main entry point for the Kick to Telegram restreaming bot.

This script orchestrates Kick channel monitoring and manages
restreaming to a Telegram group when the channel goes live.
"""
import asyncio
import signal
import sys
import argparse
import re

from . import config
from .kick_api import get_kick_stream_status
from .stream_manager import start_stream
from .telegram_manager import TelegramManager

# --- Global event for handling shutdown ---
stop_event = asyncio.Event()


def signal_handler(sig, frame):
    """Signal handler for graceful termination."""
    print("\nShutdown signal received. Terminating...")
    stop_event.set()


async def main(channel_name):
    """Main function that orchestrates the bot."""
    # Validate configuration at startup
    try:
        config.validate_config()
        print("Configuration loaded and validated successfully.")
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    # Initialize Telegram manager
    tg_manager = TelegramManager()
    await tg_manager.start()

    is_streaming = False
    
    try:
        while not stop_event.is_set():
            if not is_streaming:
                # 1. Check if channel is live
                print("==================================================")
                status, m3u8_url = get_kick_stream_status(channel_name)

                if status == "live":
                    print("✅ STREAM IS LIVE. Starting restream...")
                    # 2. Start call and restream
                    call_started = await tg_manager.start_group_call()
                    if call_started:
                        ffmpeg_process = start_stream(m3u8_url)
                        is_streaming = True
                        print("🚀 Restream started. Monitoring FFmpeg...")
                        
                        # Wait for FFmpeg to finish (async blocking)
                        while ffmpeg_process.poll() is None and not stop_event.is_set():
                            await asyncio.sleep(1)

                        print("⏹️ FFmpeg has finished.")
                        if ffmpeg_process.poll() is not None and not stop_event.is_set():
                             print("Probable cause: The streamer has ended the broadcast.")
                        
                        # 3. End the call
                        await tg_manager.end_group_call()
                        is_streaming = False
                        
                        # 4. Start cooldown period
                        if not stop_event.is_set():
                            print(f"🥶 Starting {config.COOLDOWN_SECONDS} second cooldown period...")
                            await asyncio.sleep(config.COOLDOWN_SECONDS)

                elif status == "offline":
                    print(f"⏳ Stream offline. Next check in {config.CHECK_INTERVAL_SECONDS} seconds.")
                    await asyncio.sleep(config.CHECK_INTERVAL_SECONDS)
                
                else:  # status == "error"
                    print(f"⚠️ Error checking status. Next check in {config.CHECK_INTERVAL_SECONDS} seconds.")
                    await asyncio.sleep(config.CHECK_INTERVAL_SECONDS)

            else:
                # This case shouldn't happen if logic is correct, but just in case
                print("Waiting for current restream to finish...")
                await asyncio.sleep(5)

    except asyncio.CancelledError:
        print("Main task cancelled.")
    finally:
        print("\n🧹 Performing final cleanup...")
        # Ensure Telegram call is closed on exit
        if is_streaming or tg_manager.call:
            await tg_manager.end_group_call()
        await tg_manager.disconnect()
        print("Cleanup complete.")


def run():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Monitors a Kick.com channel and restreams it to Telegram.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("channel_name", help="The Kick.com channel name to monitor.")
    args = parser.parse_args()

    # Validate channel name
    if not args.channel_name or not re.match(r"^[a-zA-Z0-9_-]+$", args.channel_name):
        print("Error: Invalid channel name. Only letters, numbers, hyphens and underscores are allowed.")
        sys.exit(1)
        
    print(f"Starting monitoring for channel: {args.channel_name}")

    # Configure signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run asyncio event loop
    try:
        asyncio.run(main(args.channel_name))
    except (KeyboardInterrupt, SystemExit):
        print("Program terminated.")


if __name__ == "__main__":
    run()
