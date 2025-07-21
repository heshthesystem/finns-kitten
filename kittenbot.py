import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
import asyncio
from flask import Flask

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot intents and commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

current_count = 1

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

ALLOWED_CHANNELS = [1396575946105946174]  

@bot.event
async def on_message(message):
    global current_count

    if message.author.bot:
        return

    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))

        if number == current_count:
            await asyncio.sleep(0.5)  
            await message.add_reaction("✅")
            current_count += 1
        else:
            await asyncio.sleep(0.5)  
            await message.add_reaction("❌")
            await message.channel.send(
                f"Wow. {message.author.mention} ruined it at {number}. We have to start over from 1 again. How sad."
            )
            current_count = 1
    else:
        await bot.process_commands(message)

# Create a simple HTTP server for Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread

    # Run the bot in a separate thread
    bot_thread = Thread(target=lambda: bot.run(TOKEN))
    bot_thread.start()

    # Get the port from the environment variable
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0",