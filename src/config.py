# -*- coding: utf-8 -*-
"""
Configuration module for loading environment variables and other parameters.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found. Make sure it exists and contains the required variables.")

# --- Telegram Variables ---
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
GROUP_ID = os.getenv('GROUP_ID')
SESSION_NAME = 'session.session'

# --- Stream Variables ---
RTMP_DEST = os.getenv('RTMP_DEST')

# --- Timing Settings ---
CHECK_INTERVAL_SECONDS = 30
COOLDOWN_SECONDS = 60

# --- Validation ---
def validate_config():
    """Validates that all required environment variables are loaded."""
    global API_ID, GROUP_ID
    required_vars = {
        'API_ID': API_ID,
        'API_HASH': API_HASH,
        'PHONE': PHONE,
        'GROUP_ID': GROUP_ID,
        'RTMP_DEST': RTMP_DEST
    }
    missing_vars = [key for key, value in required_vars.items() if value is None]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}. Check your .env file.")

    # Convert to integers if needed
    try:
        API_ID = int(API_ID)
        GROUP_ID = int(GROUP_ID)
    except (ValueError, TypeError):
        raise ValueError("API_ID and GROUP_ID must be valid integers.")
