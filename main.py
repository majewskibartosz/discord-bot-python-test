"""
Stoic Quote Discord Bot - Railway Deployment Demo

A Discord bot that dispenses Stoic wisdom from Marcus Aurelius, Seneca, and Epictetus.
Users can select a philosopher "persona" and receive quotes in that philosopher's style.

Features:
- Fetches 100 quotes from stoic-quotes.com on startup
- Groups quotes by author
- Allows users to select a philosopher persona
- Provides quotes from the selected philosopher
- Simulates the philosopher's style in greeting messages
"""

import os
import random
import aiohttp
import discord
from discord.ext import commands, tasks
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

STOIC_API_URL = "https://stoic-quotes.com/api/quotes?num=100"

# Author greetings - simulating each philosopher's unique style
AUTHOR_GREETINGS = {
    "Marcus Aurelius": [
        "Greetings, fellow traveler of life. I am **Marcus Aurelius**, Emperor of Rome and student of philosophy. Remember: the present moment is all we truly possess.",
        "Hail, seeker of wisdom. I am **Marcus Aurelius**. Like you, I struggle daily with the practice of virtue. Let us reflect together.",
        "Welcome. I am **Marcus Aurelius**. Every morning I prepare myself for the challenges ahead. Now, let us face this day with courage and reason.",
    ],
    "Seneca": [
        "Ah, a visitor! I am **Seneca**, advisor, playwright, and one who strives daily to live what he teaches. Time is our most precious resource—let us not waste it.",
        "Greetings, friend. I am **Seneca**. Though I have counseled emperors, I remain a student of life. What wisdom shall we uncover together?",
        "Welcome to this exchange of minds. I am **Seneca**. Fate leads the willing, and drags along the unwilling—which shall you be?",
    ],
    "Epictetus": [
        "So, you seek wisdom? I am **Epictetus**, once a slave, now a teacher. Remember: it is not things that disturb us, but our judgments about things.",
        "Greetings, student. I am **Epictetus**. I was born in chains, but my mind was always free. Let me show you the power of distinguishing what is in your control.",
        "Ah, another seeker! I am **Epictetus**. The lecture hall is open. First lesson: focus only on what depends on you.",
    ],
}

# Default persona when no author is selected
DEFAULT_PERSONA = "Marcus Aurelius"

# Bot activity statuses for Rich Presence (rotating)
ACTIVITIES = [
    discord.Activity(type=discord.ActivityType.watching, name="over your thoughts"),
    discord.Activity(type=discord.ActivityType.listening, name="Seneca"),
    discord.Activity(type=discord.ActivityType.playing, name="The Stoic Game"),
    discord.Activity(type=discord.ActivityType.competing, name="Rome"),
]

# Footer configuration for embeds
FOOTER_TEXT = "🚂 Powered by Stoic Wisdom • Railway Deployment"

# ═══════════════════════════════════════════════════════════════════════════════
# BOT SETUP
# ═══════════════════════════════════════════════════════════════════════════════

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Storage for quotes grouped by author
quotes_by_author: dict[str, list[str]] = defaultdict(list)

# Storage for user personas (user_id -> author_name)
user_personas: dict[int, str] = {}

# ═══════════════════════════════════════════════════════════════════════════════
# QUOTE FETCHING
# ═══════════════════════════════════════════════════════════════════════════════

async def fetch_quotes():
    """Fetch 100 quotes from the Stoic Quotes API and group by author."""
    global quotes_by_author
    
    async with aiohttp.ClientSession() as session:
        async with session.get(STOIC_API_URL) as response:
            if response.status == 200:
                quotes = await response.json()
                
                # Group quotes by author
                for quote in quotes:
                    author = quote.get("author", "Unknown")
                    text = quote.get("text", "")
                    if text:
                        quotes_by_author[author].append(text)
                
                # Log the results
                total = sum(len(q) for q in quotes_by_author.values())
                print(f"📚 Loaded {total} quotes from {len(quotes_by_author)} authors:")
                for author, author_quotes in quotes_by_author.items():
                    print(f"   • {author}: {len(author_quotes)} quotes")
            else:
                print(f"❌ Failed to fetch quotes: HTTP {response.status}")

# ═══════════════════════════════════════════════════════════════════════════════
# EVENTS
# ═══════════════════════════════════════════════════════════════════════════════

def set_embed_footer(embed: discord.Embed, additional_text: str = None) -> discord.Embed:
    """Set consistent footer on all embeds with optional additional text."""
    if additional_text:
        footer_text = f"{additional_text} | {FOOTER_TEXT}"
    else:
        footer_text = FOOTER_TEXT
    embed.set_footer(text=footer_text)
    return embed


@tasks.loop(minutes=5)
async def rotate_activity():
    """Rotate the bot's Rich Presence activity every 5 minutes."""
    activity = random.choice(ACTIVITIES)
    await bot.change_presence(activity=activity)


@bot.event
async def on_ready():
    """Called when the bot successfully connects to Discord."""
    print(f"✅ {bot.user} is online!")
    print(f"📊 Connected to {len(bot.guilds)} guild(s)")
    print(f"🐍 Python version: {os.sys.version}")
    print("📖 Fetching Stoic quotes...")
    await fetch_quotes()
    
    # Set initial activity and start rotation
    initial_activity = random.choice(ACTIVITIES)
    await bot.change_presence(activity=initial_activity)
    print(f"🎮 Activity set: {initial_activity.type.name} {initial_activity.name}")
    
    if not rotate_activity.is_running():
        rotate_activity.start()
    
    print("🏛️ Stoic Quote Bot is ready!")

# ═══════════════════════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

@bot.command(name="authors")
async def list_authors(ctx):
    """List all available philosopher personas."""
    if not quotes_by_author:
        await ctx.send("⏳ Quotes are still loading. Please try again in a moment.")
        return
    
    embed = discord.Embed(
        title="🏛️ Available Philosophers",
        description="Choose a philosopher persona to receive their wisdom.\nUse `!persona <name>` to select one.",
        color=discord.Color.gold()
    )
    
    for author, quotes in sorted(quotes_by_author.items()):
        # Get a sample quote for each author
        sample = quotes[0][:100] + "..." if len(quotes[0]) > 100 else quotes[0]
        embed.add_field(
            name=f"📜 {author} ({len(quotes)} quotes)",
            value=f"*\"{sample}\"*",
            inline=False
        )
    
    # Show current persona
    current = user_personas.get(ctx.author.id, DEFAULT_PERSONA)
    set_embed_footer(embed, f"Your current persona: {current}")
    
    await ctx.send(embed=embed)


@bot.command(name="persona")
async def set_persona(ctx, *, author_name: str = None):
    """Set your philosopher persona. Usage: !persona <author name>"""
    if not quotes_by_author:
        await ctx.send("⏳ Quotes are still loading. Please try again in a moment.")
        return
    
    if not author_name:
        current = user_personas.get(ctx.author.id, DEFAULT_PERSONA)
        await ctx.send(f"Your current persona is **{current}**. Use `!persona <author name>` to change it.")
        return
    
    # Find matching author (case-insensitive partial match)
    matching_author = None
    author_lower = author_name.lower()
    
    for author in quotes_by_author.keys():
        if author_lower in author.lower() or author.lower() in author_lower:
            matching_author = author
            break
    
    if not matching_author:
        available = ", ".join(quotes_by_author.keys())
        await ctx.send(f"❌ Philosopher not found: **{author_name}**\nAvailable: {available}")
        return
    
    # Set the persona
    user_personas[ctx.author.id] = matching_author
    
    # Get a greeting in the philosopher's style
    greetings = AUTHOR_GREETINGS.get(matching_author, [f"Hello, I am **{matching_author}**."])
    greeting = random.choice(greetings)
    
    embed = discord.Embed(
        title=f"🎭 Persona Changed",
        description=greeting,
        color=discord.Color.purple()
    )
    set_embed_footer(embed, f"Use !quote to receive wisdom from {matching_author}")
    
    await ctx.send(embed=embed)


@bot.command(name="quote")
async def get_quote(ctx):
    """Get a random quote from your selected philosopher."""
    if not quotes_by_author:
        await ctx.send("⏳ Quotes are still loading. Please try again in a moment.")
        return
    
    # Get user's current persona
    current_author = user_personas.get(ctx.author.id, DEFAULT_PERSONA)
    
    # Get quotes for this author
    author_quotes = quotes_by_author.get(current_author, [])
    
    if not author_quotes:
        await ctx.send(f"❌ No quotes available for {current_author}.")
        return
    
    # Select a random quote
    quote = random.choice(author_quotes)
    
    # Create a beautiful embed
    embed = discord.Embed(
        description=f"*\"{quote}\"*",
        color=discord.Color.blue()
    )
    embed.set_author(name=f"📜 {current_author}")
    set_embed_footer(embed, "Use !quote for another, or !persona to change philosopher")
    
    await ctx.send(embed=embed)


@bot.command(name="random")
async def random_quote(ctx):
    """Get a random quote from any philosopher."""
    if not quotes_by_author:
        await ctx.send("⏳ Quotes are still loading. Please try again in a moment.")
        return
    
    # Select a random author and quote
    author = random.choice(list(quotes_by_author.keys()))
    quote = random.choice(quotes_by_author[author])
    
    embed = discord.Embed(
        description=f"*\"{quote}\"*",
        color=discord.Color.teal()
    )
    embed.set_author(name=f"📜 {author}")
    set_embed_footer(embed, "Use !persona to follow this philosopher")
    
    await ctx.send(embed=embed)


@bot.command(name="help")
async def help_command(ctx):
    """Display available bot commands."""
    embed = discord.Embed(
        title="🏛️ Stoic Quote Bot Commands",
        description="Dispense wisdom from the great Stoic philosophers",
        color=discord.Color.green()
    )
    
    commands_list = [
        ("!authors", "List all available philosophers and their quote counts"),
        ("!persona <name>", "Select a philosopher persona (e.g., `!persona Marcus`)"),
        ("!quote", "Get a random quote from your selected philosopher"),
        ("!random", "Get a random quote from any philosopher"),
        ("!help", "Show this help message"),
        ("!ping", "Check bot latency"),
        ("!info", "Display bot information"),
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    # Show current persona
    current = user_personas.get(ctx.author.id, DEFAULT_PERSONA)
    set_embed_footer(embed, f"Your current persona: {current}")
    
    await ctx.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx):
    """Simple ping command to test if bot is responsive."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")


@bot.command(name="info")
async def info(ctx):
    """Display bot info including Python version."""
    embed = discord.Embed(
        title="🏛️ Stoic Quote Bot Information",
        description="A Discord bot that dispenses Stoic wisdom",
        color=discord.Color.blue()
    )
    embed.add_field(name="Python Version", value=os.sys.version.split()[0], inline=True)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    embed.add_field(name="Guilds", value=str(len(bot.guilds)), inline=True)
    
    # Quote stats
    total_quotes = sum(len(q) for q in quotes_by_author.values())
    embed.add_field(name="Total Quotes", value=str(total_quotes), inline=True)
    embed.add_field(name="Philosophers", value=str(len(quotes_by_author)), inline=True)
    set_embed_footer(embed)
    
    await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point for the bot."""
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
        print("Please set the DISCORD_TOKEN variable in Railway dashboard.")
        return
    
    print("🚀 Starting Stoic Quote Bot...")
    bot.run(token)


if __name__ == "__main__":
    main()
