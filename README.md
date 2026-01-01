# kick2telegram

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Automatically restream Kick.com channels to Telegram groups.**

This bot monitors a Kick.com channel and automatically starts a Telegram group video call when the streamer goes live, restreaming the content via RTMP.

## ✨ Features

- 🔄 **Auto-detection** - Monitors Kick channels and detects when they go live
- 📺 **Telegram Group Calls** - Automatically starts/ends video calls in Telegram groups
- 🎬 **RTMP Streaming** - Uses FFmpeg for reliable video transcoding
- 💬 **Chat Overlay** *(optional)* - Display live Kick chat on the stream
- ⏳ **Cooldown System** - Prevents rapid reconnection attempts

## 📋 Prerequisites

- **Python 3.9+**
- **FFmpeg** - [Download](https://ffmpeg.org/download.html) and add to PATH
- **Streamlink** *(optional, for chat overlay)* - `pip install streamlink`
- **Telegram API credentials** - Get from [my.telegram.org](https://my.telegram.org)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kick2telegram.git
   cd kick2telegram
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## ⚙️ Configuration

Edit `.env` with your credentials:

| Variable | Description |
|----------|-------------|
| `API_ID` | Telegram API ID from my.telegram.org |
| `API_HASH` | Telegram API Hash from my.telegram.org |
| `PHONE` | Your phone number with country code |
| `GROUP_ID` | Target Telegram group ID |
| `RTMP_DEST` | RTMP URL from Telegram group call settings |

### Getting the RTMP URL

1. Open your Telegram group
2. Start a video chat
3. Click **⋮** → **Stream with...**
4. Copy the RTMP URL and Stream Key

### Getting the Group ID

Add [@userinfobot](https://t.me/userinfobot) to your group and it will display the group ID.

## 📖 Usage

### Basic Usage

```bash
python -m src.main <channel_name>
```

**Example:**
```bash
python -m src.main xqc
```

### With Chat Overlay *(experimental)*

The chat module can be used to overlay live chat on your stream. See `src/chat/` for implementation details.

## 📁 Project Structure

```
kick2telegram/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration loader
│   ├── kick_api.py          # Kick.com API client
│   ├── stream_manager.py    # FFmpeg process manager
│   ├── telegram_manager.py  # Telegram client
│   └── chat/
│       ├── listener.py      # WebSocket chat listener
│       └── overlay.py       # Chat overlay for FFmpeg
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes. Ensure you have the right to restream content and comply with Kick.com's Terms of Service.
