# 🏛️ Stoic Quote Discord Bot

A Discord bot that dispenses Stoic wisdom from **Marcus Aurelius**, **Seneca**, and **Epictetus**. Users can select a philosopher "persona" and receive quotes in that philosopher's unique style.

## ✨ Features

- **100 Quotes** - Fetches and caches quotes from [stoic-quotes.com](https://stoic-quotes.com) on startup
- **Grouped by Author** - Quotes organized by philosopher for easy selection
- **Persona System** - Select a philosopher and receive wisdom in their voice
- **Styled Greetings** - Each philosopher greets you in their unique style
- **Beautiful Embeds** - Rich Discord embeds for a polished experience

---

## 📜 Commands

| Command | Description |
|---------|-------------|
| `!authors` | List all available philosophers and their quote counts |
| `!persona <name>` | Select a philosopher persona (e.g., `!persona Marcus`) |
| `!quote` | Get a random quote from your selected philosopher |
| `!random` | Get a random quote from any philosopher |
| `!help` | Show all available commands |
| `!ping` | Check bot latency |
| `!info` | Display bot information |

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/discord-bot-python-test.git
cd discord-bot-python-test
```

### 2. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" → Add Bot → Copy Token
4. Go to "OAuth2" → URL Generator → Select `bot` scope → Select permissions:
   - Send Messages
   - Embed Links
   - Read Message History
5. Copy the generated URL and invite the bot to your server

### 3. Deploy to Railway

1. Push to GitHub
2. Create new Railway project from repo
3. Add environment variable: `DISCORD_TOKEN=your_bot_token`
4. Deploy!

---

## 🐍 Python Version (Important!)

This project includes a `.python-version` file set to **Python 3.12** to avoid the `audioop` error on Python 3.13.

If you experience the error:
```
ModuleNotFoundError: No module named 'audioop'
```

See the [fixes/](./fixes/) folder for solutions.

---

## 📁 Project Structure

```
discord-bot-python-test/
├── main.py              # Stoic Quote Bot code
├── requirements.txt     # py-cord + aiohttp
├── .python-version      # Pins Python to 3.12
├── README.md           # This file
├── .gitignore          # Standard Python gitignore
└── fixes/              # Alternative fix options
    ├── .python-version
    ├── requirements-with-audioop-lts.txt
    └── mise.toml
```

---

## 🏛️ The Philosophers

### Marcus Aurelius (121-180 AD)
Roman Emperor and Stoic philosopher. His "Meditations" are private notes to himself on Stoic philosophy.

### Seneca (4 BC - 65 AD)
Roman Stoic philosopher, statesman, and dramatist. Advisor to Emperor Nero. Known for his letters on ethics and natural philosophy.

### Epictetus (50-135 AD)
Born a slave, became one of the most influential Stoic philosophers. His teachings focus on what is "in our control" vs what is not.

---

## 🔧 Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set token
export DISCORD_TOKEN="your_bot_token"

# Run
python main.py
```

---

## 📚 API Credit

Quotes provided by [stoic-quotes.com](https://stoic-quotes.com) - A free API for Stoic quotes.

---

## 📄 License

MIT License - Feel free to use and modify!
