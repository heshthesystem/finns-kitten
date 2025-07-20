import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

# Load .env variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Track the current count
current_count = 1

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_message(message):
    global current_count

    # Ignore bot's own messages
    if message.author.bot:
        return

    # Match messages that look like "meow1", "meow2", etc.
    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))

        if number == current_count:
            await message.add_reaction("✅")
            current_count += 1
        else:
            await message.add_reaction("❌")
            await message.channel.send(
                f"Wow. {message.author.mention} ruined it at {number}. We have to start over from 1 again. How sad."
            )
            current_count = 1
    else:
        # Let other commands still work
        await bot.process_commands(message)

bot.run("MTM5NjQyNzQxMjc2OTYwNzcxMA.GmfHnt.87wtO6CIemWDm0reQvPC7UFCcGGj4iIEC168AM")
