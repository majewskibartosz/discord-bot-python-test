"""
Discord Bot - Railway audioop Error Test

This minimal Discord bot is designed to reproduce the Python 3.13 + audioop 
crash that occurs on Railway when no Python version is pinned.

The error occurs because:
1. Railway's Railpack defaults to Python 3.13
2. Python 3.13 removed the 'audioop' module from the standard library (PEP 594)
3. Discord libraries (py-cord, discord.py) still import audioop for voice features

To reproduce the error:
- Deploy this project without a .python-version file
- The bot will crash with: ModuleNotFoundError: No module named 'audioop'

To fix the error, use one of these solutions:
1. Add a .python-version file with "3.11" 
2. Set RAILPACK_PACKAGES=python@3.11 in Railway variables
3. Add 'audioop-lts' to requirements.txt
"""

import os
import discord
from discord.ext import commands

# Setup intents - required for modern Discord.py/Pycord
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Called when the bot successfully connects to Discord."""
    print(f"✅ {bot.user} is online!")
    print(f"📊 Connected to {len(bot.guilds)} guild(s)")
    print(f"🐍 Python version: {os.sys.version}")


@bot.command(name="ping")
async def ping(ctx):
    """Simple ping command to test if bot is responsive."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")


@bot.command(name="info")
async def info(ctx):
    """Display bot info including Python version."""
    embed = discord.Embed(
        title="Bot Information",
        description="Railway audioop Test Bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="Python Version", value=os.sys.version.split()[0], inline=True)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    embed.add_field(name="Guilds", value=str(len(bot.guilds)), inline=True)
    await ctx.send(embed=embed)


@bot.command(name="help")
async def help_command(ctx):
    """Display available bot commands."""
    embed = discord.Embed(
        title="Bot Commands",
        description="Available commands for this Discord bot",
        color=discord.Color.green()
    )
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!info", value="Display bot information", inline=False)
    embed.add_field(name="!help", value="Show this help message", inline=False)
    await ctx.send(embed=embed)


def main():
    """Main entry point for the bot."""
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
        print("Please set the DISCORD_TOKEN variable in Railway dashboard.")
        return
    
    print("🚀 Starting Discord bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
