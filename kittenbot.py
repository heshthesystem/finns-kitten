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
last_user = None  # Track the last user who counted

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

ALLOWED_CHANNELS = [1396575946105946174]  

@bot.event
async def on_message(message):
    global current_count, last_user

    if message.author.bot:
        return

    # Ensure the message is in the allowed channel
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    # Match messages that look like "meow1", "meow2", etc.
    match = re.fullmatch(r"meow(\d+)", message.content.strip().lower())
    if match:
        number = int(match.group(1))

        # Prevent the same user from counting twice consecutively
        if message.author.id == last_user:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("⚠️") # Add the yellow exclamation mark emoji
            await message.channel.send(
                f"{message.author.mention}, you can't count twice in a row, idiot! That wouldn't be fair to the other nerds who want to count. Not that I care. But it *is* a bit selfish, so if you do, I'll just ignore your message and not count it. So there! Ha! Take that, asshole!"
            )
            return

        if number == current_count:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("✅")
            current_count += 1
            last_user = message.author.id  # Update the last user
        else:
            await asyncio.sleep(1)  # Add a short delay to avoid rate limits
            await message.add_reaction("❌")
            await message.channel.send(
                f"Wow. {message.author.mention} ruined it at {number}. What a loser! Now we have to start over from 1 again. How embarrassing! You should be ashamed of yourself. I mean, really, how hard is it to count to {current_count}? It's not rocket science! But noooo, you had to mess it up. So now we have to start over. Thanks a lot, jerk!"
            )
            current_count = 1
            last_user = None  # Reset the last user
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
    app.run(host="0.0.0.0", port=port)