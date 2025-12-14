# 🏛️ Stoic Quote Discord Bot

![Gemini_Generated_Image_scwwijscwwijscww](https://github.com/user-attachments/assets/b60f4038-0853-48b0-af93-77a853a84a10)


A Discord bot that dispenses Stoic wisdom from **Marcus Aurelius**, **Seneca**, and **Epictetus**. Users can select a philosopher "persona" and receive quotes in that philosopher's unique style.

[**Install Link - Use this link to add Stoic Quote Bot to your Discord server.**](https://discord.com/oauth2/authorize?client_id=1449043709906784486)


## ✨ Features

- **100 Quotes** - Fetches and caches quotes from [stoic-quotes.com](https://stoic-quotes.com) on startup
- **Philosopher Personas** - Select your favorite philosopher (Marcus Aurelius, Seneca, or Epictetus) and receive wisdom in their voice
- **Rich Presence** - Dynamic activity status that rotates every 5 minutes, showcasing philosophical themes
- **Philosopher Biographies** - Detailed historical information about each philosopher with their teachings and legacy
- **Welcome Messages** - Automatic personalized greetings when the bot joins a new server
- **Consistent Branding** - Roman-themed gold/bronze color scheme across all embeds with custom footers
- **Beautiful Embeds** - Styled Discord embeds with philosopher emojis and rich formatting

---

## 📜 Commands

| Command | Description |
|---------|-------------|
| `!authors` | List all available philosophers and their quote counts with sample wisdom |
| `!persona <name>` | Select a philosopher persona (e.g., `!persona Marcus` or `!persona Seneca`) |
| `!quote` | Get a random quote from your selected philosopher |
| `!random` | Get a random quote from any philosopher |
| `!bio` | Learn about your selected philosopher's life, teachings, and historical significance |
| `!help` | Show all available commands and current persona |
| `!ping` | Check bot latency |
| `!info` | Display bot information including quote statistics and connected servers |

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

## 🐍 Python Version

This project runs on **Python 3.11** (or newer) and uses Railway's built-in Python support.

### About `.python-version` Files

We do **NOT** include a `.python-version` file because it triggers `mise` (version manager) which can cause SSL certificate verification errors in some CI/CD environments like Railway:

```
mise ERROR error:0A000086:SSL routines:tls_post_process_server_certificate:
certificate verify failed (hostname mismatch)
```

**Solution**: Let Railway use its default Python installation instead. No action needed - the deployment will work automatically.

### Python 3.13 Note

If you need to use this bot with Python 3.13+, you may encounter:
```
ModuleNotFoundError: No module named 'audioop'
```

See the [fixes/](./fixes/) folder for solutions (add `audioop-lts` to requirements or use the provided `mise.toml`).

---

## 📁 Project Structure

```
discord-bot-python-test/
├── main.py                          # Stoic Quote Bot code
├── requirements.txt                 # py-cord + aiohttp dependencies
├── README.md                        # This file
├── .gitignore                       # Standard Python gitignore
└── fixes/                           # Alternative configurations for different environments
    ├── .python-version              # Pin Python to specific version (triggers mise)
    ├── requirements-with-audioop-lts.txt  # Alternative for Python 3.13+
    └── mise.toml                    # Mise configuration (alternative to .python-version)
```

---

## 🏛️ The Philosophers

### 👑 Marcus Aurelius (121-180 AD)
**Roman Emperor & Stoic Philosopher**

Roman Emperor and Stoic philosopher. His *Meditations* are private notes to himself on Stoic philosophy, written during military campaigns. He is considered the last of the Five Good Emperors. His reflections on duty, virtue, and acceptance remain deeply influential today.

### 📝 Seneca (4 BC - 65 AD)
**Stoic Philosopher & Statesman**

Roman Stoic philosopher, statesman, and dramatist. Advisor to Emperor Nero. Known for his letters on ethics and natural philosophy. His works on anger, tranquility, and the shortness of life remain influential. He believed philosophy should be practical and improve how we live.

### ⛓️ Epictetus (50-135 AD)
**Stoic Philosopher & Former Slave**

Born a slave, became one of the most influential Stoic philosophers. His teachings focus on what is *in our control* vs what is not. His philosophy emphasizes acceptance and inner freedom. He taught that while we cannot control external events, we have complete control over our judgments and responses.

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
