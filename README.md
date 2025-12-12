# Discord Bot - Railway Python 3.13 audioop Error Test

This project demonstrates a common Railway deployment issue where Discord bots crash immediately on startup with:

```
ModuleNotFoundError: No module named 'audioop'
```

## 🔍 The Problem

When deploying a Discord bot to Railway without specifying a Python version:

1. **Railway's Railpack** defaults to **Python 3.13**
2. **Python 3.13** removed the `audioop` module from the standard library ([PEP 594](https://peps.python.org/pep-0594/))
3. **Discord libraries** (py-cord, discord.py) still import `audioop` for voice features
4. **Result**: Immediate crash on startup

### Error Screenshot

The traceback shows the path `/app/.venv/lib/python3.13/site-packages/discord/player.py` trying to `import audioop`:

```
File "/app/.venv/lib/python3.13/site-packages/discord/player.py", line 29, in <module>
    import audioop
ModuleNotFoundError: No module named 'audioop'
```

---

## 🐛 How to Reproduce the Error

### Deploy to Railway (Broken Version)

1. Push this project to a GitHub repository
2. Create a new Railway project from the repo
3. Set the `DISCORD_TOKEN` environment variable in Railway
4. Deploy — the bot will crash with the `audioop` error

**Important**: Make sure there is NO `.python-version` file in the repo!

---

## ✅ How to Fix

Choose ONE of the following solutions:

### Option 1: Pin Python Version (Recommended)

Add a `.python-version` file to your project root:

```text
3.11
```

This file is auto-detected by Railway's Railpack builder (which uses Mise).

### Option 2: Use Environment Variable

In the Railway dashboard, add this Service Variable:

| Variable Name | Value |
|--------------|-------|
| `RAILPACK_PACKAGES` | `python@3.11` |

### Option 3: Use audioop-lts Package

If you want to stay on Python 3.13, add the backport package to `requirements.txt`:

```text
py-cord>=2.4.0
audioop-lts
```

---

## 📁 Project Structure

```
discord-bot-python-test/
├── main.py              # Discord bot code
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .python-version     # [ADD THIS TO FIX] Python version pin
```

---

## 🚀 Railway Deployment Steps

### Step 1: Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit - Discord bot"
git remote add origin https://github.com/YOUR_USERNAME/discord-bot-python-test.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Create a new project → Deploy from GitHub repo
3. Select your repository
4. Add environment variable: `DISCORD_TOKEN=your_bot_token_here`
5. Deploy!

### Step 3: Fix the Error

After seeing the error, add the `.python-version` file:

```bash
echo "3.11" > .python-version
git add .python-version
git commit -m "Fix: Pin Python version to 3.11 to avoid audioop error"
git push
```

Railway will automatically redeploy with Python 3.11.

---

## 📚 Technical Background

### What is audioop?

`audioop` was a Python standard library module for manipulating raw audio data. It was deprecated in Python 3.11 and removed in Python 3.13 as part of [PEP 594 - "Dead Batteries"](https://peps.python.org/pep-0594/).

### Why does Discord need audioop?

Discord.py and its forks (py-cord, nextcord) use `audioop` for:
- Voice channel audio processing
- Audio volume adjustment
- PCM audio manipulation

### What is audioop-lts?

[audioop-lts](https://pypi.org/project/audioop-lts/) is a backport package that provides the removed `audioop` module for Python 3.13+.

### Railpack vs Nixpacks

Railway recently switched from **Nixpacks** to **Railpack** as the default builder:

| Feature | Nixpacks (Legacy) | Railpack (Current) |
|---------|-------------------|-------------------|
| Version File | `nixpacks.toml` | `.python-version` or `mise.toml` |
| Env Variable | `NIXPACKS_PYTHON_VERSION` | `RAILPACK_PACKAGES` |
| Format | `python311` | `python@3.11` |

---

## 🔗 Resources

- [Railway Build Configuration Docs](https://docs.railway.com/guides/build-configuration)
- [Railpack GitHub](https://github.com/railwayapp/railpack)
- [PEP 594 - Removing Dead Batteries](https://peps.python.org/pep-0594/)
- [audioop-lts on PyPI](https://pypi.org/project/audioop-lts/)
- [Mise Version Manager](https://mise.jdx.dev/)
